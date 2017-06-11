#!/usr/bin/python
"""User Database"""
from userbase_config import config
import psycopg2
import cStringIO
import traceback
import userbase_models
import userbase_validations
import bcrypt
import datetime
import uuid

class Database:

    def __init__(self, salt, fn_log_error, config_path, config_section='postgresql'):
        self.salt = salt
        self.grp_admin = "Admin"
        self.fn_log_error = fn_log_error
        self.config = config(config_path, config_section)

    #salt = "DummyUserbaseSalt"
    #grp_admin = "Admin"

    def id_from_username(self, username):
        """ finds id_user from username """
        conn = None
        id = 0
        try:
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE name = %(name)s AND active = true",
                        {
                            "name": username
                        })
            row = cur.fetchone()

            if row is not None:
                id = int(row[0])

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error("There was an error: {0}".format(traceback.format_exc()))
        finally:
            if conn is not None:
                conn.close()
        return id

    def id_from_email(self, email):
        """ finds id_user from email """
        conn = None
        id = 0
        try:
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("SELECT u.id FROM user_authentications ua JOIN users u ON u.id = ua.id WHERE recovery_email = %(email)s AND active = true",
                        {
                            "email": email
                        })
            row = cur.fetchone()

            if row is not None:
                id = int(row[0])

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error("There was an error: {0}".format(traceback.format_exc()))
        finally:
            if conn is not None:
                conn.close()
        return id

    def username_exists(self, username):
        """ checks if username exists """
        return self.id_from_username(username) > 0

    def email_exists(self, email):
        """ checks if email exists """
        return self.id_from_email(email) > 0

    def create_user(self, rq):
        """ creates user """
        if self.username_exists(rq.Username) or self.email_exists(rq.Authentication.Email):
            return userbase_models.ConnectUserResponse.invalid()
        
        if (
                not userbase_validations.username(rq.Username) or
                not userbase_validations.email(rq.Authentication.Email) or
                not userbase_validations.password(rq.Authentication.Password) or
                not userbase_validations.display_name(rq.Profile.DisplayName)
            ):
            return userbase_models.ConnectUserResponse.invalid()

        id_user = self.__create_user_entity(rq)
        self.__create_authentication_entity(rq, id_user)
        self.__create_profile_entity(rq, id_user)
        self.__create_setting_entity(rq, id_user)

        return self.__get_summary(self.__create_connection_token_response(id_user))

    def validate_credentials(self, username, password):
        """ validate user credentials """
        resp = userbase_models.ConnectUserResponse.invalid()
        
        id_user = self.id_from_username(username)
        if id_user == 0:
            return resp

        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("SELECT password FROM user_authentications WHERE id = %(id)s",
                        {
                            "id": id_user
                        })
            row = cur.fetchone()

            if row is not None:
                dbpass = row[0]
                if bcrypt.checkpw(bytes(self.__salt_password(password)), bytes(dbpass)):
                    resp = self.__create_connection_token_response(id_user)

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error("There was an error: {0}".format(traceback.format_exc()))
        finally:
            if conn is not None:
                conn.close()
        return self.__get_summary(resp)

    def disconnect(self, username, token):
        """ disconnect """
        resp = False
        conn_resp = self.__validate_connection_token_response(username, token)
        if not conn_resp.Success:
            return resp

        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("UPDATE user_tokens SET Expiration = %(expiration)s WHERE id_user = %(id)s AND token = %(token)s",
                        {
                            "id": conn_resp.IdUser,
                            "token": token,
                            "expiration": datetime.datetime.now()
                        })
            cur.close()
            resp = True
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error("There was an error: {0}".format(traceback.format_exc()))
        finally:
            if conn is not None:
                conn.close()
        return resp

    def deactivate(self, username, token):
        """ deactivate """
        resp = False
        conn_resp = self.__validate_connection_token_response(username, token)
        if not conn_resp.Success:
            return resp

        self.disconnect(username, token)

        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("UPDATE users SET Active = false WHERE id = %(id)s",
                        {
                            "id": conn_resp.IdUser
                        })
            cur.close()
            resp = True
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error("There was an error: {0}".format(traceback.format_exc()))
        finally:
            if conn is not None:
                conn.close()
        return resp

    def modify_credentials(self, username, token, creds):
        """ modify_credentials """
        conn_resp = self.__validate_connection_token_response(username, token)
        resp = userbase_models.TokenSuccessResponse(conn_resp.Success, conn_resp.Token)

        if not resp.Success:
            return resp

        if len(creds.Password) > 0:
            if not userbase_validations.password(creds.Password):
                resp = userbase_models.TokenSuccessResponse.invalid()
            else:
                conn = None
                try:
                    hashed_password = bcrypt.hashpw(bytes(self.__salt_password(creds.Password)), bcrypt.gensalt())
                    conn = psycopg2.connect(**self.config)
                    cur = conn.cursor()
                    cur.execute("UPDATE user_authentications SET password = %(password)s WHERE id = %(id)s",
                                {
                                    "id": conn_resp.IdUser,
                                    "password": hashed_password
                                })
                    cur.close()
                    conn.commit()
                except (Exception, psycopg2.DatabaseError) as error:
                    self.fn_log_error("There was an error: {0}".format(traceback.format_exc()))
                    resp = userbase_models.TokenSuccessResponse.invalid()
                finally:
                    if conn is not None:
                        conn.close()

        if not resp.Success:
            return resp

        if len(creds.Email) > 0:
            if not userbase_validations.email(creds.Email):
                resp = userbase_models.TokenSuccessResponse.invalid()
            else:
                conn = None
                try:
                    conn = psycopg2.connect(**self.config)
                    cur = conn.cursor()
                    cur.execute("UPDATE user_authentications SET recovery_email = %(email)s WHERE id = %(id)s",
                                {
                                    "id": conn_resp.IdUser,
                                    "email": creds.Email
                                })
                    cur.close()
                    conn.commit()
                except (Exception, psycopg2.DatabaseError) as error:
                    self.fn_log_error("There was an error: {0}".format(traceback.format_exc()))
                    resp = userbase_models.TokenSuccessResponse.invalid()
                finally:
                    if conn is not None:
                        conn.close()

        return resp

    def modify_profile(self, username, token, prof):
        """ modify_profile """
        conn_resp = self.__validate_connection_token_response(username, token)
        resp = userbase_models.TokenSuccessResponse(conn_resp.Success, conn_resp.Token)

        if not resp.Success:
            return resp

        if len(prof.DisplayName) > 0:
            if not userbase_validations.display_name(prof.DisplayName):
                resp = userbase_models.TokenSuccessResponse.invalid()
            else:
                conn = None
                try:
                    conn = psycopg2.connect(**self.config)
                    cur = conn.cursor()
                    cur.execute("UPDATE user_profiles SET display_name = %(display)s WHERE id = %(id)s",
                                {
                                    "id": conn_resp.IdUser,
                                    "display": prof.DisplayName
                                })
                    cur.close()
                    conn.commit()
                except (Exception, psycopg2.DatabaseError) as error:
                    self.fn_log_error("There was an error: {0}".format(traceback.format_exc()))
                    resp = userbase_models.TokenSuccessResponse.invalid()
                finally:
                    if conn is not None:
                        conn.close()

        return resp

    def send_recovery(self, username, send_email_func):
        """ send_recovery """
        resp = False
        
        id_user = self.id_from_username(username)
        if id_user == 0:
            return resp

        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("SELECT recovery_email FROM user_authentications WHERE id = %(id)s",
                        {
                            "id": id_user
                        })
            row = cur.fetchone()

            if row is not None:
                email = row[0]
            cur.close()

            send_email_func(self.__create_recovery_token_response(id_user).Token, email, self.fn_log_error)

            resp = True
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error("There was an error: {0}".format(traceback.format_exc()))
        finally:
            if conn is not None:
                conn.close()
        return resp

    def reset_password(self, username, token, password):
        """ reset_password """
        id_user = self.id_from_username(username)
        if id_user == 0:
            return userbase_models.ConnectUserResponse.invalid()

        if not userbase_validations.password(password):
            return userbase_models.ConnectUserResponse.invalid()

        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("SELECT expiration FROM user_recovery_tokens WHERE id_user = %(id)s AND token = %(token)s",
                        {
                            "id": id_user,
                            "token": token
                        })
            row = cur.fetchone()
            cur.close()

            if row is not None:
                expiration = row[0]
                if expiration > datetime.datetime.now():
                    new_token = userbase_models.Token(token, datetime.datetime.now())
                    cur2 = conn.cursor()
                    cur2.execute("UPDATE user_recovery_tokens SET Expiration = %(expiration)s WHERE id_user = %(id)s AND token = %(token)s",
                                {
                                    "id": id_user,
                                    "token": new_token.Id,
                                    "expiration": new_token.ValidUntil
                                })
                    cur2.close()

                    hashed_password = bcrypt.hashpw(bytes(self.__salt_password(password)), bcrypt.gensalt())

                    cur3 = conn.cursor()
                    cur3.execute("UPDATE user_authentications SET password = %(password)s WHERE id = %(id)s",
                                {
                                    "id": id_user,
                                    "password": hashed_password
                                })
                    cur3.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error("There was an error: {0}".format(traceback.format_exc()))
        finally:
            if conn is not None:
                conn.close()
        return self.validate_credentials(username, password)

    def list_users(self, username, token):
        """ list_users """
        resp = userbase_models.ConnectUserResponse.invalid()
        conn_resp = self.__validate_connection_token_response(username, token)
        if not conn_resp.Success:
            return resp

        if not self.__is_user_in_group(conn_resp.IdUser, self.grp_admin):
            return resp

        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("SELECT u.id, u.name, up.display_name FROM users u NATURAL JOIN user_profiles up WHERE u.active = true")
            row = cur.fetchone()
            users = []
            while row is not None:
                users.append(userbase_models.User(int(row[0]), row[1], row[2], self.__get_groups(int(row[0]))))
                row = cur.fetchone()
            resp = userbase_models.UserListResponse(True, conn_resp.Token, users)
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error("There was an error: {0}".format(traceback.format_exc()))
        finally:
            if conn is not None:
                conn.close()
        return resp

    def include_in_group(self, rq):
        """ include_in_group """
        resp = userbase_models.ConnectUserResponse.invalid()
        conn_resp = self.__validate_connection_token_response(rq.Username, rq.Token)
        if not conn_resp.Success:
            return resp

        if not self.__is_user_in_group(conn_resp.IdUser, self.grp_admin):
            return resp

        id_user_to_add = self.id_from_username(rq.UserToAdd)
        if id_user_to_add == 0:
            return resp

        if self.__is_user_in_groupid(id_user_to_add, rq.IdGroup):
            return resp

        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("INSERT INTO user_groups (id_user, id_user_group_type) VALUES (%(id_user)s,%(id_group)s)",
                        {
                            "id_user": id_user_to_add,
                            "id_group": rq.IdGroup
                        })
            cur.close()
            conn.commit()
            resp = conn_resp
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error("There was an error: {0}".format(traceback.format_exc()))
        finally:
            if conn is not None:
                conn.close()
        return self.__get_summary(resp)

    def exclude_from_group(self, username, token, user_to_remove, id_group):
        """ exclude_from_group """
        resp = userbase_models.ConnectUserResponse.invalid()
        conn_resp = self.__validate_connection_token_response(username, token)
        if not conn_resp.Success:
            return resp

        if not self.__is_user_in_group(conn_resp.IdUser, self.grp_admin):
            return resp

        id_user_to_add = self.id_from_username(user_to_remove)
        if id_user_to_add == 0:
            return resp

        if not self.__is_user_in_groupid(id_user_to_add, id_group):
            return resp

        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("DELETE FROM user_groups WHERE id_user = %(id_user)s AND id_user_group_type = %(id_group)s",
                        {
                            "id_user": id_user_to_add,
                            "id_group": id_group
                        })
            cur.close()
            conn.commit()
            resp = conn_resp
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error("There was an error: {0}".format(traceback.format_exc()))
        finally:
            if conn is not None:
                conn.close()
        return self.__get_summary(resp)

    def __create_user_entity(self, rq):
        conn = None
        id = 0
        try:
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("INSERT INTO users (name,active) VALUES (%(name)s, true) RETURNING id;",
                        {
                            "name": rq.Username
                        })
            row = cur.fetchone()

            if row is not None:
                id = int(row[0])

            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error(error)
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return id

    def __create_authentication_entity(self, rq, id_user):
        hashed_password = bcrypt.hashpw(bytes(self.__salt_password(rq.Authentication.Password)), bcrypt.gensalt())
        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("INSERT INTO user_authentications (id,password,recovery_email) VALUES (%(id)s, %(pass)s, %(email)s);",
                        {
                            "id": id_user,
                            "pass": hashed_password,
                            "email": rq.Authentication.Email
                        })
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error(error)
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def __create_profile_entity(self, rq, id_user):
        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("INSERT INTO user_profiles (id,display_name) VALUES (%(id)s, %(display)s);",
                        {
                            "id": id_user,
                            "display": rq.Profile.DisplayName
                        })
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error(error)
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def __create_setting_entity(self, rq, id_user):
        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("INSERT INTO user_settings (id,id_user_access_type_list_friends) VALUES (%(id)s, 1);",
                        {
                            "id": id_user
                        })
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error(error)
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def __create_connection_token_response(self, id_user):
        resp = userbase_models.ConnectUserResponse.invalid()
        conn = None
        try:
            token = userbase_models.Token(str(uuid.uuid4()), datetime.datetime.now() + datetime.timedelta(minutes=10))
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("INSERT INTO user_tokens (id_user,token,expiration) VALUES (%(id)s, %(token)s, %(expiration)s);",
                        {
                            "id": id_user,
                            "token": token.Id,
                            "expiration": token.ValidUntil
                        })
            cur.close()
            conn.commit()
            resp = userbase_models.ConnectUserResponse(True, token, id_user)
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error(error)
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return resp

    def __create_recovery_token_response(self, id_user):
        resp = userbase_models.ConnectUserResponse.invalid()
        conn = None
        try:
            token = userbase_models.Token(str(uuid.uuid4()), datetime.datetime.now() + datetime.timedelta(days=1))
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("INSERT INTO user_recovery_tokens (id_user,token,expiration) VALUES (%(id)s, %(token)s, %(expiration)s);",
                        {
                            "id": id_user,
                            "token": token.Id,
                            "expiration": token.ValidUntil
                        })
            cur.close()
            conn.commit()
            resp = userbase_models.ConnectUserResponse(True, token, id_user)
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error(error)
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return resp

    def __validate_connection_token_response(self, username, token):
        """ validate user credentials """
        resp = userbase_models.ConnectUserResponse.invalid()
        
        id_user = self.id_from_username(username)
        if id_user == 0:
            return resp

        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("SELECT expiration FROM user_tokens WHERE id_user = %(id)s AND token = %(token)s",
                        {
                            "id": id_user,
                            "token": token
                        })
            row = cur.fetchone()
            cur.close()

            if row is not None:
                expiration = row[0]
                if expiration > datetime.datetime.now():
                    new_token = userbase_models.Token(token, datetime.datetime.now() + datetime.timedelta(minutes=10))
                    cur2 = conn.cursor()
                    cur2.execute("UPDATE user_tokens SET Expiration = %(expiration)s WHERE id_user = %(id)s AND token = %(token)s",
                                {
                                    "id": id_user,
                                    "token": new_token.Id,
                                    "expiration": new_token.ValidUntil
                                })
                    cur2.close()
                    resp = userbase_models.ConnectUserResponse(True, new_token, id_user)
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error("There was an error: {0}".format(traceback.format_exc()))
        finally:
            if conn is not None:
                conn.close()
        return resp

    def __get_summary(self, conn_resp):
        """ validate user credentials """
        return  userbase_models.UserSummaryResponse(True, conn_resp.Token, self.__get_profile(conn_resp.IdUser), self.__get_groups(conn_resp.IdUser))

    def __get_profile(self, id_user):
        """ validate user credentials """
        profile = userbase_models.ProfileInfo(None)
        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("SELECT display_name FROM user_profiles WHERE id = %(id)s",
                        {
                            "id": id_user
                        })
            row = cur.fetchone()
            cur.close()

            if row is not None:
                profile = userbase_models.ProfileInfo(row[0])
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error("There was an error: {0}".format(traceback.format_exc()))
        finally:
            if conn is not None:
                conn.close()
        return profile

    def __get_groups(self, id_user):
        """ __get_groups """
        groups = []
        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            cur = conn.cursor()
            cur.execute("SELECT ugt.id, name FROM user_groups ug JOIN user_group_types ugt ON ug.id_user_group_type = ugt.id WHERE id_user = %(id)s",
                        {
                            "id": id_user
                        })
            row = cur.fetchone()
            while row is not None:
                groups.append(userbase_models.Group(int(row[0]), row[1]))
                row = cur.fetchone()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.fn_log_error("There was an error: {0}".format(traceback.format_exc()))
        finally:
            if conn is not None:
                conn.close()
        return groups

    def __is_user_in_group(self, id_user, group):
        """ __is_user_in_group """
        groups = self.__get_groups(id_user)
        for grp in groups:
            if grp.Name == group:
                return True
        return False

    def __is_user_in_groupid(self, id_user, id_group):
        """ __is_user_in_groupid """
        groups = self.__get_groups(id_user)
        for grp in groups:
            if grp.Id == id_group:
                return True
        return False


    def __salt_password(self, password):
        return self.salt + password
