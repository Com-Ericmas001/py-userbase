import datetime

class AuthenticationInfo:
    def __init__(self, password, email):
        self.Password = password
        self.Email = email

class ProfileInfo:
    def __init__(self, display_name):
        self.DisplayName = display_name

class Token:
    def __init__(self, id_token, valid_until):
        self.Id = id_token
        self.ValidUntil = valid_until

class User:
    def __init__(self, id_user, username, display_name, groups):
        self.IdUser = id_user
        self.Username = username
        self.DisplayName = display_name
        self.Groups = groups

class Group:
    def __init__(self, id_group, name):
        self.Id = id_group
        self.Name = name

class CreateUserRequest:
    def __init__(self, username, authentication, profile):
        self.Username = username
        self.Authentication = authentication
        self.Profile = profile

class ModifyCredentialsRequest:
    def __init__(self, username, token, authentication):
        self.Username = username
        self.Token = token
        self.Authentication = authentication

class ModifyProfileRequest:
    def __init__(self, username, token, profile):
        self.Username = username
        self.Token = token
        self.Profile = profile

class AddUserToGroupRequest:
    def __init__(self, username, token, user_to_add, id_group):
        self.Username = username
        self.Token = token
        self.UserToAdd = user_to_add
        self.IdGroup = id_group

class TokenSuccessResponse:
    def __init__(self, success, token):
        self.Success = success
        self.Token = token

    @staticmethod
    def invalid():
        return TokenSuccessResponse(
            False,
            Token("", datetime.datetime.now()))

class ConnectUserResponse:
    def __init__(self, success, token, id_user):
        self.Success = success
        self.Token = token
        self.IdUser = id_user

    @staticmethod
    def invalid():
        return ConnectUserResponse(
            False,
            Token("", datetime.datetime.now()),
            0)


class UserSummaryResponse:
    def __init__(self, success, token, display_name, groups):
        self.Success = success
        self.Token = token
        self.DisplayName = display_name
        self.Groups = groups

    @staticmethod
    def invalid():
        return UserSummaryResponse(
            False,
            Token("", datetime.datetime.now()),
            "", [])

class UserListResponse:
    def __init__(self, success, token, users):
        self.Success = success
        self.Token = token
        self.Users = users

    @staticmethod
    def invalid():
        return UserListResponse(
            False,
            Token("", datetime.datetime.now()),
            [])
