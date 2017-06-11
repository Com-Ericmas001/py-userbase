--- CHANGE MY_USERBASE_USER for your user

DROP TABLE user_settings;
DROP TABLE user_access_types;
DROP TABLE user_authentications;
DROP TABLE user_groups;
DROP TABLE user_group_types;
DROP TABLE user_profiles;
DROP TABLE user_recovery_tokens;
DROP TABLE user_relation_types;
DROP TABLE user_tokens;
DROP TABLE users;

DROP SEQUENCE user_access_types_seq;
DROP SEQUENCE user_group_types_seq;
DROP SEQUENCE user_groups_seq;
DROP SEQUENCE user_recovery_tokens_seq;
DROP SEQUENCE user_relation_types_seq;
DROP SEQUENCE user_relations_seq;
DROP SEQUENCE user_tokens_seq;
DROP SEQUENCE users_seq;



CREATE SEQUENCE user_access_types_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 4
  CACHE 1;
ALTER TABLE user_access_types_seq
  OWNER TO postgres;
GRANT ALL ON SEQUENCE user_access_types_seq TO postgres;
GRANT ALL ON SEQUENCE user_access_types_seq TO MY_USERBASE_USER;


CREATE SEQUENCE user_group_types_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE user_group_types_seq
  OWNER TO postgres;
GRANT ALL ON SEQUENCE user_group_types_seq TO postgres;
GRANT ALL ON SEQUENCE user_group_types_seq TO MY_USERBASE_USER;


CREATE SEQUENCE user_groups_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE user_groups_seq
  OWNER TO postgres;
GRANT ALL ON SEQUENCE user_groups_seq TO postgres;
GRANT ALL ON SEQUENCE user_groups_seq TO MY_USERBASE_USER;


CREATE SEQUENCE user_recovery_tokens_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE user_recovery_tokens_seq
  OWNER TO postgres;
GRANT ALL ON SEQUENCE user_recovery_tokens_seq TO postgres;
GRANT ALL ON SEQUENCE user_recovery_tokens_seq TO MY_USERBASE_USER;


CREATE SEQUENCE user_relation_types_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE user_relation_types_seq
  OWNER TO postgres;
GRANT ALL ON SEQUENCE user_relation_types_seq TO postgres;
GRANT ALL ON SEQUENCE user_relation_types_seq TO MY_USERBASE_USER;


CREATE SEQUENCE user_relations_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE user_relations_seq
  OWNER TO postgres;
GRANT ALL ON SEQUENCE user_relations_seq TO postgres;
GRANT ALL ON SEQUENCE user_relations_seq TO MY_USERBASE_USER;


CREATE SEQUENCE user_tokens_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE user_tokens_seq
  OWNER TO postgres;
GRANT ALL ON SEQUENCE user_tokens_seq TO postgres;
GRANT ALL ON SEQUENCE user_tokens_seq TO MY_USERBASE_USER;


CREATE SEQUENCE users_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE users_seq
  OWNER TO postgres;
GRANT ALL ON SEQUENCE users_seq TO postgres;
GRANT ALL ON SEQUENCE users_seq TO MY_USERBASE_USER;



--
-- TOC entry 187 (class 1259 OID 24699)
-- Name: user_access_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE user_access_types (
    id integer DEFAULT nextval('user_access_types_seq'::regclass) NOT NULL,
    name text NOT NULL,
    value integer NOT NULL
);


ALTER TABLE user_access_types OWNER TO postgres;

--
-- TOC entry 190 (class 1259 OID 24771)
-- Name: user_authentications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE user_authentications (
    id integer NOT NULL,
    password text NOT NULL,
    recovery_email text NOT NULL
);


ALTER TABLE user_authentications OWNER TO postgres;

--
-- TOC entry 194 (class 1259 OID 24842)
-- Name: user_group_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE user_group_types (
    id integer DEFAULT nextval('user_group_types_seq'::regclass) NOT NULL,
    name text NOT NULL
);


ALTER TABLE user_group_types OWNER TO postgres;

--
-- TOC entry 195 (class 1259 OID 25011)
-- Name: user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE user_groups (
    id integer DEFAULT nextval('user_groups_seq'::regclass) NOT NULL,
    id_user integer NOT NULL,
    id_user_group_type integer NOT NULL
);


ALTER TABLE user_groups OWNER TO postgres;

--
-- TOC entry 191 (class 1259 OID 24784)
-- Name: user_profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE user_profiles (
    id integer NOT NULL,
    display_name text NOT NULL
);


ALTER TABLE user_profiles OWNER TO postgres;

--
-- TOC entry 197 (class 1259 OID 25055)
-- Name: user_recovery_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE user_recovery_tokens (
    id integer DEFAULT nextval('user_recovery_tokens_seq'::regclass) NOT NULL,
    id_user integer NOT NULL,
    token text NOT NULL,
    expiration timestamp without time zone NOT NULL
);


ALTER TABLE user_recovery_tokens OWNER TO postgres;

--
-- TOC entry 188 (class 1259 OID 24717)
-- Name: user_relation_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE user_relation_types (
    id integer DEFAULT nextval('user_relation_types_seq'::regclass) NOT NULL,
    name text NOT NULL
);


ALTER TABLE user_relation_types OWNER TO postgres;

--
-- TOC entry 192 (class 1259 OID 24797)
-- Name: user_settings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE user_settings (
    id integer NOT NULL,
    id_user_access_type_list_friends integer NOT NULL
);


ALTER TABLE user_settings OWNER TO postgres;

--
-- TOC entry 196 (class 1259 OID 25027)
-- Name: user_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE user_tokens (
    id integer DEFAULT nextval('user_tokens_seq'::regclass) NOT NULL,
    id_user integer NOT NULL,
    token text NOT NULL,
    expiration timestamp without time zone NOT NULL
);


ALTER TABLE user_tokens OWNER TO postgres;

--
-- TOC entry 189 (class 1259 OID 24762)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE users (
    id integer DEFAULT nextval('users_seq'::regclass) NOT NULL,
    name text NOT NULL,
    active boolean NOT NULL
);


ALTER TABLE users OWNER TO postgres;

--
-- TOC entry 1969 (class 2606 OID 24707)
-- Name: pk_user_access_types; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_access_types
    ADD CONSTRAINT pk_user_access_types PRIMARY KEY (id);


--
-- TOC entry 1975 (class 2606 OID 24778)
-- Name: pk_user_authentications; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_authentications
    ADD CONSTRAINT pk_user_authentications PRIMARY KEY (id);


--
-- TOC entry 1981 (class 2606 OID 24850)
-- Name: pk_user_group_types; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_group_types
    ADD CONSTRAINT pk_user_group_types PRIMARY KEY (id);


--
-- TOC entry 1983 (class 2606 OID 25016)
-- Name: pk_user_groups; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_groups
    ADD CONSTRAINT pk_user_groups PRIMARY KEY (id);


--
-- TOC entry 1977 (class 2606 OID 24791)
-- Name: pk_user_profiles; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_profiles
    ADD CONSTRAINT pk_user_profiles PRIMARY KEY (id);


--
-- TOC entry 1987 (class 2606 OID 25063)
-- Name: pk_user_recovery_tokens; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_recovery_tokens
    ADD CONSTRAINT pk_user_recovery_tokens PRIMARY KEY (id);


--
-- TOC entry 1971 (class 2606 OID 24725)
-- Name: pk_user_relation_types; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_relation_types
    ADD CONSTRAINT pk_user_relation_types PRIMARY KEY (id);


--
-- TOC entry 1979 (class 2606 OID 24801)
-- Name: pk_user_settings; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_settings
    ADD CONSTRAINT pk_user_settings PRIMARY KEY (id);


--
-- TOC entry 1985 (class 2606 OID 25035)
-- Name: pk_user_tokens; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_tokens
    ADD CONSTRAINT pk_user_tokens PRIMARY KEY (id);


--
-- TOC entry 1973 (class 2606 OID 24770)
-- Name: pk_users; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT pk_users PRIMARY KEY (id);


--
-- TOC entry 1988 (class 2606 OID 24779)
-- Name: fk_user_authentications_users; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_authentications
    ADD CONSTRAINT fk_user_authentications_users FOREIGN KEY (id) REFERENCES users(id);


--
-- TOC entry 1992 (class 2606 OID 25017)
-- Name: fk_user_groups_user_group_types; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_groups
    ADD CONSTRAINT fk_user_groups_user_group_types FOREIGN KEY (id_user_group_type) REFERENCES user_group_types(id);


--
-- TOC entry 1993 (class 2606 OID 25022)
-- Name: fk_user_groups_users; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_groups
    ADD CONSTRAINT fk_user_groups_users FOREIGN KEY (id_user) REFERENCES users(id);


--
-- TOC entry 1989 (class 2606 OID 24792)
-- Name: fk_user_profiles_users; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_profiles
    ADD CONSTRAINT fk_user_profiles_users FOREIGN KEY (id) REFERENCES users(id);


--
-- TOC entry 1995 (class 2606 OID 25064)
-- Name: fk_user_recovery_tokens_users; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_recovery_tokens
    ADD CONSTRAINT fk_user_recovery_tokens_users FOREIGN KEY (id_user) REFERENCES users(id);


--
-- TOC entry 1991 (class 2606 OID 24807)
-- Name: fk_user_settings_user_access_types; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_settings
    ADD CONSTRAINT fk_user_settings_user_access_types FOREIGN KEY (id_user_access_type_list_friends) REFERENCES user_access_types(id);


--
-- TOC entry 1990 (class 2606 OID 24802)
-- Name: fk_user_settings_users; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_settings
    ADD CONSTRAINT fk_user_settings_users FOREIGN KEY (id) REFERENCES users(id);


--
-- TOC entry 1994 (class 2606 OID 25036)
-- Name: fk_user_tokens_users; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_tokens
    ADD CONSTRAINT fk_user_tokens_users FOREIGN KEY (id_user) REFERENCES users(id);


--
-- TOC entry 2109 (class 0 OID 0)
-- Dependencies: 187
-- Name: user_access_types; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE user_access_types FROM PUBLIC;
REVOKE ALL ON TABLE user_access_types FROM postgres;
GRANT ALL ON TABLE user_access_types TO postgres;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE user_access_types TO MY_USERBASE_USER;


--
-- TOC entry 2110 (class 0 OID 0)
-- Dependencies: 190
-- Name: user_authentications; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE user_authentications FROM PUBLIC;
REVOKE ALL ON TABLE user_authentications FROM postgres;
GRANT ALL ON TABLE user_authentications TO postgres;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE user_authentications TO MY_USERBASE_USER;


--
-- TOC entry 2111 (class 0 OID 0)
-- Dependencies: 194
-- Name: user_group_types; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE user_group_types FROM PUBLIC;
REVOKE ALL ON TABLE user_group_types FROM postgres;
GRANT ALL ON TABLE user_group_types TO postgres;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE user_group_types TO MY_USERBASE_USER;


--
-- TOC entry 2112 (class 0 OID 0)
-- Dependencies: 195
-- Name: user_groups; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE user_groups FROM PUBLIC;
REVOKE ALL ON TABLE user_groups FROM postgres;
GRANT ALL ON TABLE user_groups TO postgres;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE user_groups TO MY_USERBASE_USER;


--
-- TOC entry 2113 (class 0 OID 0)
-- Dependencies: 191
-- Name: user_profiles; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE user_profiles FROM PUBLIC;
REVOKE ALL ON TABLE user_profiles FROM postgres;
GRANT ALL ON TABLE user_profiles TO postgres;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE user_profiles TO MY_USERBASE_USER;


--
-- TOC entry 2114 (class 0 OID 0)
-- Dependencies: 197
-- Name: user_recovery_tokens; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE user_recovery_tokens FROM PUBLIC;
REVOKE ALL ON TABLE user_recovery_tokens FROM postgres;
GRANT ALL ON TABLE user_recovery_tokens TO postgres;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE user_recovery_tokens TO MY_USERBASE_USER;


--
-- TOC entry 2115 (class 0 OID 0)
-- Dependencies: 188
-- Name: user_relation_types; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE user_relation_types FROM PUBLIC;
REVOKE ALL ON TABLE user_relation_types FROM postgres;
GRANT ALL ON TABLE user_relation_types TO postgres;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE user_relation_types TO MY_USERBASE_USER;


--
-- TOC entry 2116 (class 0 OID 0)
-- Dependencies: 192
-- Name: user_settings; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE user_settings FROM PUBLIC;
REVOKE ALL ON TABLE user_settings FROM postgres;
GRANT ALL ON TABLE user_settings TO postgres;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE user_settings TO MY_USERBASE_USER;


--
-- TOC entry 2117 (class 0 OID 0)
-- Dependencies: 196
-- Name: user_tokens; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE user_tokens FROM PUBLIC;
REVOKE ALL ON TABLE user_tokens FROM postgres;
GRANT ALL ON TABLE user_tokens TO postgres;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE user_tokens TO MY_USERBASE_USER;


--
-- TOC entry 2118 (class 0 OID 0)
-- Dependencies: 189
-- Name: users; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE users FROM PUBLIC;
REVOKE ALL ON TABLE users FROM postgres;
GRANT ALL ON TABLE users TO postgres;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE users TO MY_USERBASE_USER;






-- Data for Name: user_access_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO user_access_types VALUES (1, 'Everybody', 10);
INSERT INTO user_access_types VALUES (2, 'EverybodyNotBlocked', 20);
INSERT INTO user_access_types VALUES (3, 'Friends', 30);
INSERT INTO user_access_types VALUES (4, 'JustMe', 40);
ALTER SEQUENCE user_access_types_seq RESTART WITH 5;

-- Data for Name: user_group_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO user_group_types VALUES (1, 'Admin');
ALTER SEQUENCE user_group_types_seq RESTART WITH 2;


-- Data for Name: user_relation_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO user_relation_types VALUES (1, 'Friend');
INSERT INTO user_relation_types VALUES (2, 'Blocked');
ALTER SEQUENCE user_relation_types_seq RESTART WITH 3;
