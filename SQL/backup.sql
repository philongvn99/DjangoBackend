--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3
-- Dumped by pg_dump version 12.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


--
-- Name: accounttypes; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.accounttypes AS ENUM (
    'ADMIN',
    'USER',
    'GUESY'
);


ALTER TYPE public.accounttypes OWNER TO postgres;

--
-- Name: player_statuses; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.player_statuses AS ENUM (
    'ACTIVE',
    'LOAN',
    'LEFT'
);


ALTER TYPE public.player_statuses OWNER TO postgres;

--
-- Name: roles; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.roles AS ENUM (
    'GOALKEEPER',
    'DEFENDER',
    'MIDFIELDER',
    'FORWARD'
);


ALTER TYPE public.roles OWNER TO postgres;

--
-- Name: infotype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.infotype AS (
	id integer,
	name character varying(256),
	full_name character varying(256),
	avatar_link character varying(256),
	nationality character varying(30),
	birthday date,
	right_foot boolean,
	kit_number integer,
	height integer,
	role public.roles,
	salary integer,
	status public.player_statuses
);


ALTER TYPE public.infotype OWNER TO postgres;

--
-- Name: leagues; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.leagues AS ENUM (
    'CHAMPIONS_LEAGUE',
    'EUROPA_LEAGUE',
    'PREMIER_LEAGUE',
    'FA_CUP',
    'CARABAO_CUP'
);


ALTER TYPE public.leagues OWNER TO postgres;

--
-- Name: matchtypes; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.matchtypes AS ENUM (
    'EPL_LEAGUE',
    'EUL_GROUP_STATE',
    'UCL_GROUP_STATE',
    'FA_ROUND',
    'EFL_ROUND',
    'EUL_ROUND_OF_32',
    'EUL_ROUND_OF_16',
    'UCL_ROUND_OF_16',
    'EUL_QUARTER_FINAL',
    'UCL_QUARTER_FINAL',
    'FA_SEMI_FINAL',
    'EFL_SEMI_FINAL',
    'EUL_SEMI_FINAL',
    'UCL_SEMI_FINAL',
    'FA_FINAL',
    'EFL_FINAL',
    'EUL_FINAL',
    'UCL_FINAL'
);


ALTER TYPE public.matchtypes OWNER TO postgres;

--
-- Name: user_return_info; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.user_return_info AS (
	username character varying(256),
	email character varying(256),
	phone character varying(256),
	name character varying(256)
);


ALTER TYPE public.user_return_info OWNER TO postgres;

--
-- Name: authenticate_user(character varying, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.authenticate_user(user_name character varying, user_password character varying) RETURNS public.user_return_info
    LANGUAGE plpgsql
    AS $$
	DECLARE 
		user_info user_return_info DEFAULT NULL;
	BEGIN
		SELECT account_username AS username, account_email AS email, account_phone AS phone, account_name AS "name"
			INTO user_info
			FROM tb_account
			WHERE ((account_username = user_name) OR (account_phone = user_name) OR (account_phone = user_name)) AND (account_password = user_password);
		RETURN user_info;
	END;
	$$;


ALTER FUNCTION public.authenticate_user(user_name character varying, user_password character varying) OWNER TO postgres;

--
-- Name: clear_league_table(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.clear_league_table() RETURNS TABLE(tname character varying, played_game integer, win_game integer, drawn_game integer, lost_game integer, goal_for integer, goal_against integer, goal_difference integer, points integer)
    LANGUAGE plpgsql
    AS $$
	BEGIN
		UPDATE tb_team SET
				team_played_game = 0,
				team_win_game = 0,
				team_drawn_game = 0,
				team_lost_game = 0,
				team_goal_for = 0,
				team_goal_against = 0,
				team_goal_difference = 0,
				team_points = 0;
		RETURN QUERY 
				SELECT 
					team_name,
					team_played_game,
					team_win_game,
					team_drawn_game,
					team_lost_game,
					team_goal_for,
					team_goal_against,
					team_goal_difference,
					team_points 
				FROM tb_team ;
	END
	$$;


ALTER FUNCTION public.clear_league_table() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: tb_team; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_team (
    team_id integer NOT NULL,
    team_name character varying(256),
    team_acronym_name character varying(256),
    team_logo_link character varying(256),
    team_played_game integer DEFAULT 0 NOT NULL,
    team_win_game integer DEFAULT 0 NOT NULL,
    team_drawn_game integer DEFAULT 0 NOT NULL,
    team_lost_game integer DEFAULT 0 NOT NULL,
    team_goal_for integer DEFAULT 0 NOT NULL,
    team_goal_against integer DEFAULT 0 NOT NULL,
    team_goal_difference integer DEFAULT 0 NOT NULL,
    team_points integer DEFAULT 0 NOT NULL,
    league public.leagues DEFAULT 'PREMIER_LEAGUE'::public.leagues NOT NULL
);


ALTER TABLE public.tb_team OWNER TO postgres;

--
-- Name: get_all_teams(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_all_teams() RETURNS SETOF public.tb_team
    LANGUAGE plpgsql
    AS $$
BEGIN
   RETURN QUERY
   SELECT * FROM tb_team 
   ORDER BY team_points DESC, 
   			team_goal_difference DESC,
			team_goal_for DESC,
			team_goal_against ASC,
			team_name ASC;
END
$$;


ALTER FUNCTION public.get_all_teams() OWNER TO postgres;

--
-- Name: get_player_by_id(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_player_by_id(p_id integer) RETURNS SETOF public.infotype
    LANGUAGE plpgsql
    AS $$
		BEGIN
			RETURN QUERY
				SELECT *
				FROM  tb_player
				WHERE player_id = "p_id";
		END
	$$;


ALTER FUNCTION public.get_player_by_id(p_id integer) OWNER TO postgres;

--
-- Name: get_user_by_username(character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_user_by_username(user_name character varying) RETURNS public.user_return_info
    LANGUAGE plpgsql
    AS $$
	DECLARE
		user_info user_return_info DEFAULT NULL;
	BEGIN
		SELECT account_username AS username, account_email AS email, account_phone AS phone, account_name AS "name"
			FROM tb_account
			INTO user_info
			WHERE (account_username = user_name) OR (account_phone = user_name) OR (account_phone = user_name);
		RETURN user_info;
	END;
	$$;


ALTER FUNCTION public.get_user_by_username(user_name character varying) OWNER TO postgres;

--
-- Name: update_league_table(integer[], integer[], integer[], integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_league_table(idlist integer[], gslist integer[], gclist integer[], nmatch integer) RETURNS TABLE(tname character varying, played_game integer, win_game integer, drawn_game integer, lost_game integer, goal_for integer, goal_against integer, goal_difference integer, points integer)
    LANGUAGE plpgsql
    AS $_$
DECLARE
    i int;
	addPts int;
	resType varchar(256);
BEGIN
	FOR i IN 1..nMatch 
	LOOP
		CASE 
			WHEN gsList[i] > gcList[i] THEN
					resType := 'team_win_game';
					addPts := 3;
			WHEN gsList[i] < gcList[i] THEN
					resType := 'team_lost_game';
					addPts := 0;
			ELSE 
				resType := 'team_drawn_game';
				addPts := 1;
		END CASE;
		EXECUTE 
			FORMAT(
			'UPDATE tb_team 
					SET 
						%1$s = %1$s + 1,
						team_played_game = team_played_game + 1,
						team_goal_for = team_goal_for + %3$s,
						team_goal_against = team_goal_against + %4$s,
						team_goal_difference = team_goal_difference + %3$s - %4$s,
						team_points = team_points + %2$s
					WHERE team_id = %5$s', resType, addPts, gsList[i], gcList[i], idList[i]);
	END LOOP;
	RETURN QUERY 
			SELECT 
				team_name,
				team_played_game,
				team_win_game,
				team_drawn_game,
				team_lost_game,
				team_goal_for,
				team_goal_against,
				team_goal_difference,
				team_points 
			FROM tb_team where team_id = ANY (idList);
END
$_$;


ALTER FUNCTION public.update_league_table(idlist integer[], gslist integer[], gclist integer[], nmatch integer) OWNER TO postgres;

--
-- Name: update_points(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_points() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	UPDATE tb_league_table SET team_points = NEW.team_win_game * 3 + NEW.team_drawn_game WHERE team_id = NEW.team_id;
	RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_points() OWNER TO postgres;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: r_goalscore; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.r_goalscore (
    gs_player_id integer,
    gs_match_id integer,
    gs_minute integer
);


ALTER TABLE public.r_goalscore OWNER TO postgres;

--
-- Name: r_owngoal; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.r_owngoal (
    og_player_id integer,
    og_match_id integer,
    og_minute integer
);


ALTER TABLE public.r_owngoal OWNER TO postgres;

--
-- Name: r_redcard; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.r_redcard (
    rc_player_id integer,
    rc_match_id integer,
    rc_minute integer
);


ALTER TABLE public.r_redcard OWNER TO postgres;

--
-- Name: r_yellowcard; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.r_yellowcard (
    yc_player_id integer,
    yc_match_id integer,
    yc_minute integer
);


ALTER TABLE public.r_yellowcard OWNER TO postgres;

--
-- Name: tb_account; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_account (
    account_id character varying(256) NOT NULL,
    account_email character varying(256) NOT NULL,
    account_username character varying(256) NOT NULL,
    account_phone character varying(256) NOT NULL,
    account_name character varying(256) NOT NULL,
    account_password character varying(256) NOT NULL,
    account_role public.accounttypes NOT NULL,
    CONSTRAINT valid_password_length CHECK ((length((account_password)::text) >= 6)),
    CONSTRAINT valid_username_length CHECK ((length((account_username)::text) >= 6))
);


ALTER TABLE public.tb_account OWNER TO postgres;

--
-- Name: tb_match; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_match (
    match_id integer NOT NULL,
    match_enemy_id integer NOT NULL,
    match_stadium character varying(256) NOT NULL,
    match_home boolean NOT NULL,
    match_home_score integer,
    match_enemy_score integer,
    match_date date,
    match_lineup character varying(5),
    match_referee character varying(256),
    match_type public.matchtypes
);


ALTER TABLE public.tb_match OWNER TO postgres;

--
-- Name: tb_match_match_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_match_match_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tb_match_match_id_seq OWNER TO postgres;

--
-- Name: tb_match_match_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_match_match_id_seq OWNED BY public.tb_match.match_id;


--
-- Name: tb_player; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_player (
    player_id integer NOT NULL,
    player_name character varying(256) NOT NULL,
    player_full_name character varying(256) NOT NULL,
    player_avatar_link character varying(256) NOT NULL,
    player_nationality character varying(30) NOT NULL,
    player_birthday date DEFAULT '2020-01-01'::date NOT NULL,
    player_right_foot boolean NOT NULL,
    player_kit_number integer NOT NULL,
    player_height integer NOT NULL,
    player_role public.roles,
    player_salary integer,
    player_status public.player_statuses
);


ALTER TABLE public.tb_player OWNER TO postgres;

--
-- Name: COLUMN tb_player.player_height; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_player.player_height IS 'positive';


--
-- Name: COLUMN tb_player.player_salary; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_player.player_salary IS 'positive';


--
-- Name: tb_player_player_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_player_player_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tb_player_player_id_seq OWNER TO postgres;

--
-- Name: tb_player_player_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_player_player_id_seq OWNED BY public.tb_player.player_id;


--
-- Name: tb_team_team_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_team_team_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tb_team_team_id_seq OWNER TO postgres;

--
-- Name: tb_team_team_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_team_team_id_seq OWNED BY public.tb_team.team_id;


--
-- Name: user_query_pass; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_query_pass (
    account_password character varying(256)
);


ALTER TABLE public.user_query_pass OWNER TO postgres;

--
-- Name: v_defenders; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.v_defenders AS
 SELECT tb_player.player_id,
    tb_player.player_name,
    tb_player.player_nationality,
    tb_player.player_birthday,
    tb_player.player_height,
    tb_player.player_role,
    tb_player.player_salary,
    tb_player.player_status
   FROM public.tb_player
  WHERE (tb_player.player_role = 'DEFENDER'::public.roles);


ALTER TABLE public.v_defenders OWNER TO postgres;

--
-- Name: v_forwards; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.v_forwards AS
 SELECT tb_player.player_id,
    tb_player.player_name,
    tb_player.player_nationality,
    tb_player.player_birthday,
    tb_player.player_height,
    tb_player.player_role,
    tb_player.player_salary,
    tb_player.player_status
   FROM public.tb_player
  WHERE (tb_player.player_role = 'FORWARD'::public.roles);


ALTER TABLE public.v_forwards OWNER TO postgres;

--
-- Name: v_goalkeepers; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.v_goalkeepers AS
 SELECT tb_player.player_id,
    tb_player.player_name,
    tb_player.player_nationality,
    tb_player.player_birthday,
    tb_player.player_height,
    tb_player.player_role,
    tb_player.player_salary,
    tb_player.player_status
   FROM public.tb_player
  WHERE (tb_player.player_role = 'GOALKEEPER'::public.roles);


ALTER TABLE public.v_goalkeepers OWNER TO postgres;

--
-- Name: v_midfielders; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.v_midfielders AS
 SELECT tb_player.player_id,
    tb_player.player_name,
    tb_player.player_nationality,
    tb_player.player_birthday,
    tb_player.player_height,
    tb_player.player_role,
    tb_player.player_salary,
    tb_player.player_status
   FROM public.tb_player
  WHERE (tb_player.player_role = 'MIDFIELDER'::public.roles);


ALTER TABLE public.v_midfielders OWNER TO postgres;

--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: tb_match match_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_match ALTER COLUMN match_id SET DEFAULT nextval('public.tb_match_match_id_seq'::regclass);


--
-- Name: tb_player player_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_player ALTER COLUMN player_id SET DEFAULT nextval('public.tb_player_player_id_seq'::regclass);


--
-- Name: tb_team team_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_team ALTER COLUMN team_id SET DEFAULT nextval('public.tb_team_team_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2021-07-12 19:06:57.138135+07
2	auth	0001_initial	2021-07-12 19:06:57.302498+07
3	admin	0001_initial	2021-07-12 19:06:57.34638+07
4	admin	0002_logentry_remove_auto_add	2021-07-12 19:06:57.363336+07
5	admin	0003_logentry_add_action_flag_choices	2021-07-12 19:06:57.378295+07
6	contenttypes	0002_remove_content_type_name	2021-07-12 19:06:57.416194+07
7	auth	0002_alter_permission_name_max_length	2021-07-12 19:06:57.433156+07
8	auth	0003_alter_user_email_max_length	2021-07-12 19:06:57.45111+07
9	auth	0004_alter_user_username_opts	2021-07-12 19:06:57.464066+07
10	auth	0005_alter_user_last_login_null	2021-07-12 19:06:57.484014+07
11	auth	0006_require_contenttypes_0002	2021-07-12 19:06:57.489014+07
12	auth	0007_alter_validators_add_error_messages	2021-07-12 19:06:57.503475+07
13	auth	0008_alter_user_username_max_length	2021-07-12 19:06:57.536387+07
14	auth	0009_alter_user_last_name_max_length	2021-07-12 19:06:57.553342+07
15	auth	0010_alter_group_name_max_length	2021-07-12 19:06:57.575284+07
16	auth	0011_update_proxy_permissions	2021-07-12 19:06:57.590243+07
17	auth	0012_alter_user_first_name_max_length	2021-07-12 19:06:57.60671+07
18	sessions	0001_initial	2021-07-12 19:06:57.631644+07
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: r_goalscore; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.r_goalscore (gs_player_id, gs_match_id, gs_minute) FROM stdin;
\.


--
-- Data for Name: r_owngoal; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.r_owngoal (og_player_id, og_match_id, og_minute) FROM stdin;
\.


--
-- Data for Name: r_redcard; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.r_redcard (rc_player_id, rc_match_id, rc_minute) FROM stdin;
\.


--
-- Data for Name: r_yellowcard; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.r_yellowcard (yc_player_id, yc_match_id, yc_minute) FROM stdin;
\.


--
-- Data for Name: tb_account; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_account (account_id, account_email, account_username, account_phone, account_name, account_password, account_role) FROM stdin;
585F072E30U	long.vonguyenphi@gmail.com	dr3g0ng44m	0327071985	Phi Long 6/3	01886933234	ADMIN
585F072E31U	dr3g0ng44m@gmail.com	dr3g0ng44n	0327071985	YooNaLimmm	binbin123	USER
6735323825U	holtby331@gmail.com	holtby331	01886933234	Elia249315	ure8582	USER
\.


--
-- Data for Name: tb_match; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_match (match_id, match_enemy_id, match_stadium, match_home, match_home_score, match_enemy_score, match_date, match_lineup, match_referee, match_type) FROM stdin;
1	9	Old Trafford	t	\N	\N	\N	\N	\N	\N
2	16	St MARRY	f	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: tb_player; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_player (player_id, player_name, player_full_name, player_avatar_link, player_nationality, player_birthday, player_right_foot, player_kit_number, player_height, player_role, player_salary, player_status) FROM stdin;
106	De Gea	David de Gea Quintana	https://resources.premierleague.com/premierleague/photos/players/250x250/p51940.png	Spain	1990-11-07	t	1	192	GOALKEEPER	375	ACTIVE
107	Dean Henderson	Dean Bradley Henderson	https://resources.premierleague.com/premierleague/photos/players/250x250/p172649.png	Endland	1997-03-12	t	26	188	GOALKEEPER	100	ACTIVE
108	Maguire	Jacob Harry Maguire	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000142/Treated_Player_Profile_Thumbnail_Maguire_11626421871630.jpg	Endland	1993-03-05	t	5	194	DEFENDER	190	ACTIVE
109	Lindelof	Victor Jorgen Nilsson Lindelof	https://resources.premierleague.com/premierleague/photos/players/250x250/p184667.png	Sweden	1994-07-17	t	2	187	DEFENDER	120	ACTIVE
110	Varane	Raphael Xavier Varane	https://assets.manutd.com/AssetPicker/images/0/0/15/121/1014053/Player_Profile_Thumbnail_RV_metadata_removed1629814324519.jpg	France	1993-04-25	t	99	191	DEFENDER	172	ACTIVE
111	Bailly	Eric Bertrand Bailly	https://resources.premierleague.com/premierleague/photos/players/250x250/p197365.png	Ivory Coast	1994-03-05	t	3	187	DEFENDER	80	ACTIVE
112	Tuanzebe	Axel Tuanzebe	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000161/Treated_Player_Profile_Thumbnail_Tuanzebe1626424466159.jpg	Congo	1997-11-14	t	38	186	DEFENDER	50	ACTIVE
113	Phil Jones	Phil Anthony Jones	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000145/Treated_Player_Profile_Thumbnail_Jones1626423306220.jpg	Endland	1992-02-21	t	4	185	DEFENDER	75	ACTIVE
114	Telles	Alex Nicolao Telles	https://assets.manutd.com/AssetPicker/images/0/0/15/55/997174/Alex_Telles_Landingpage1626421346294.jpg	Brazil	1992-12-15	t	27	181	DEFENDER	93	ACTIVE
115	Luke Shaw	Luke Paul Hoare Shaw	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000135/Treated_Player_Profile_Thumbnail_Shaw1626422466032.jpg	Endland	1995-07-12	f	23	185	DEFENDER	150	ACTIVE
116	Brandon W.	Brandon Paul Brian Williams	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000157/Treated_Player_Profile_Thumbnail_Williams1626356183344.jpg	Endland	2000-09-03	f	33	172	DEFENDER	65	ACTIVE
117	wan Bissaka	Aaron Wan-Bissaka	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000158/Treated_Player_Profile_Thumbnail_Wans_Bissaka1626355531775.jpg	Endland	1997-11-26	t	29	183	DEFENDER	90	ACTIVE
118	Diogo Dalot	Jose Diogo Dalot Teixeira	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000150/Treated_Player_Profile_Thumbnail_Dalot1626356756247.jpg	Portugal	1999-03-18	t	20	183	DEFENDER	54	ACTIVE
119	Teden Mengi	Teden Mambuene Mengi	https://assets.manutd.com/AssetPicker/images/0/0/15/55/997254/mengi_player_grid__2_1626423846616.jpg	England	2002-04-30	t	43	186	DEFENDER	1	ACTIVE
120	Matic	Nemanja Matic	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000139/Treated_Player_Profile_Thumbnail_Matic1626423129191.jpg	Serbia	1988-08-01	f	31	194	MIDFIELDER	120	ACTIVE
121	James Garner	James David Garner	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000147/Treated_Player_Profile_Thumbnail_Garner1626421974124.jpg	England	2001-03-13	t	37	182	MIDFIELDER	19	LOAN
122	Pogba	Paul Labile Pogba	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000137/Treated_Player_Profile_Thumbnail_Pogba1626423217888.jpg	France	1993-03-15	t	6	191	MIDFIELDER	290	ACTIVE
123	Van De Beek	Donny van de Beek	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000159/Treated_Player_Profile_Thumbnail_van_de_Beek1626356866391.jpg	Netherlands	1997-04-18	t	34	184	MIDFIELDER	120	ACTIVE
124	McTominay	Scott Francis McTominay	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000138/Treated_Player_Profile_Thumbnail_McTominay1626423399235.jpg	Scotland	1996-12-08	t	39	191	MIDFIELDER	20	ACTIVE
125	Fred	Frederico Rodrigues de Paula Santos	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000148/Treated_Player_Profile_Thumbnail_Fred1626421779442.jpg	Brazil	1993-03-05	f	17	169	MIDFIELDER	120	ACTIVE
126	Bruno Fernandes	Bruno Miguel Borges Fernandes	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000149/Treated_Player_Profile_Thumbnail_Fernandes1626356273672.jpg	Portugal	1994-09-08	t	18	179	MIDFIELDER	180	ACTIVE
127	Pellistri	Facundo Pellistri	https://assets.manutd.com/AssetPicker/images/0/0/15/55/997199/Facundo_Pellistri_Landingpage1626421662586.jpg	Uruguay	2001-12-20	t	28	175	MIDFIELDER	15	ACTIVE
128	Mata	Juan Manuel Mata Garcia	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000140/Treated_Player_Profile_Thumbnail_Mata_11626422203863.jpg	Spain	1988-04-28	f	8	170	MIDFIELDER	160	ACTIVE
129	Andreas Pereira	Andreas Hugo Hoelgebaum Pereira	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000154/Treated_Player_Profile_Thumbnail_A_Periera1626355847241.jpg	Brazil	1996-01-01	t	15	177	MIDFIELDER	30	LOAN
130	Hannibal	Hannibal Mejbri	https://resources.premierleague.com/premierleague/photos/players/250x250/p465527.png	Tunisia	2003-01-21	t	46	182	MIDFIELDER	0	ACTIVE
131	Lingard	Jesse Ellis Lingard	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000143/Treated_Player_Profile_Thumbnail_Lingard1626422106800.jpg	Spain	1992-12-15	t	14	175	MIDFIELDER	58	ACTIVE
132	Daniel James	Daniel Owen James	https://saybongda.com/wp-content/uploads/2021/05/Daniel-James-avt-1024x773.jpg	Wales	1997-11-10	t	21	170	FORWARD	45	LEFT
133	Rashford	Marcus Rashford MBE	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000136/Treated_Player_Profile_Thumbnail_Rashford1626422926368.jpg	Endland	1997-10-31	t	10	185	FORWARD	200	ACTIVE
134	Greenwood	Mason Will John Greenwood	https://resources.premierleague.com/premierleague/photos/players/250x250/p220688.png	Endland	2001-10-01	f	11	181	FORWARD	35	ACTIVE
135	Amad Diallo	Amad Diallo	https://assets.manutd.com/AssetPicker/images/0/0/15/55/997198/Amad_Diallo_Landingpage1626421446601.jpg	Ivory Coast	2002-07-11	f	16	173	FORWARD	48	ACTIVE
136	Sancho	Jadon Malik Sancho	https://assets.manutd.com/AssetPicker/images/0/0/15/78/1003014/Player-Profile-Thumbnail-Sancho1627370980650.jpg	England	2000-03-25	t	25	180	FORWARD	350	ACTIVE
137	Martial	Anthony Jordan Martial	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000141/Treated_Player_Profile_Thumbnail_Martial_11626355968632.jpg	France	1995-12-05	t	9	181	FORWARD	250	ACTIVE
138	Cavani	Edinson Roberto Cavani Gomez	https://assets.manutd.com/AssetPicker/images/0/0/15/55/997213/Edinson_Cavani_Landingpage1626421572829.jpg	Uruguay	1987-02-14	t	21	184	FORWARD	210	ACTIVE
139	Ronaldo	Cristian Ronaldo dos Santos Aveiro	https://resources.premierleague.com/premierleague/photos/players/250x250/p14937.png	Portugal	1990-05-02	t	7	185	FORWARD	385	ACTIVE
140	Elanga	Anthony David Junior Elanga	https://resources.premierleague.com/premierleague/photos/players/250x250/p449434.png	Sweden	2002-04-27	t	36	178	FORWARD	0	ACTIVE
141	Shoretire	Shola Maxwell Shoretire	https://resources.premierleague.com/premierleague/photos/players/250x250/p472464.png	England	2004-02-02	t	47	171	FORWARD	0	ACTIVE
142	Tahith Chong	Tahith Chong	https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000151/Treated_Player_Profile_Thumbnail_Chong1626423490987.jpg	Netherlands	1999-12-04	f	44	185	FORWARD	0	LOAN
\.


--
-- Data for Name: tb_team; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_team (team_id, team_name, team_acronym_name, team_logo_link, team_played_game, team_win_game, team_drawn_game, team_lost_game, team_goal_for, team_goal_against, team_goal_difference, team_points, league) FROM stdin;
17	Tottenham Hotspur	TOT	https://resources.premierleague.com/premierleague/badges/t6.png	18	10	3	5	23	20	3	33	PREMIER_LEAGUE
18	Watford	WAT	https://resources.premierleague.com/premierleague/badges/t57.png	18	4	1	13	22	36	-14	13	PREMIER_LEAGUE
14	Newcastle United	NEW	https://resources.premierleague.com/premierleague/badges/t4.png	19	1	8	10	19	42	-23	11	PREMIER_LEAGUE
15	Norwich City	NOR	https://resources.premierleague.com/premierleague/badges/t45.png	19	2	4	13	8	42	-34	10	PREMIER_LEAGUE
12	Manchester City	MCI	https://resources.premierleague.com/premierleague/badges/t43.png	21	17	2	2	53	13	40	53	PREMIER_LEAGUE
1	Arsenal	ARS	https://resources.premierleague.com/premierleague/badges/t3.png	20	11	2	7	33	25	8	35	PREMIER_LEAGUE
6	Chelsea	CHE	https://resources.premierleague.com/premierleague/badges/t8.png	21	12	7	2	45	16	29	43	PREMIER_LEAGUE
13	Manchester United	MUN	https://resources.premierleague.com/premierleague/badges/t1.png	19	9	4	6	30	27	3	31	PREMIER_LEAGUE
7	Crystal Palace	CRY	https://resources.premierleague.com/premierleague/badges/t31.png	20	5	8	7	29	30	-1	23	PREMIER_LEAGUE
19	West Ham United	WHU	https://resources.premierleague.com/premierleague/badges/t21.png	20	10	4	6	37	27	10	34	PREMIER_LEAGUE
5	Burnley	BUR	https://resources.premierleague.com/premierleague/badges/t90.png	17	1	8	8	16	27	-11	11	PREMIER_LEAGUE
4	Brighton and Hove Albion	BHA	https://resources.premierleague.com/premierleague/badges/t36.png	19	6	9	4	20	20	0	27	PREMIER_LEAGUE
3	Brenford	BRE	https://resources.premierleague.com/premierleague/badges/t94.png	19	6	5	8	23	26	-3	23	PREMIER_LEAGUE
2	Aston Villa	AVL	https://resources.premierleague.com/premierleague/badges/t7.png	19	7	1	11	25	30	-5	22	PREMIER_LEAGUE
16	Southamton	SOU	https://resources.premierleague.com/premierleague/badges/t20.png	19	4	9	6	20	29	-9	21	PREMIER_LEAGUE
10	Leicester City	LEI	https://resources.premierleague.com/premierleague/badges/t13.png	18	7	4	7	30	33	-3	25	PREMIER_LEAGUE
11	Liverpool	LIV	https://resources.premierleague.com/premierleague/badges/t14.png	20	12	6	2	52	18	34	42	PREMIER_LEAGUE
9	Leeds United	LEE	https://resources.premierleague.com/premierleague/badges/t2.png	19	4	7	8	21	37	-16	19	PREMIER_LEAGUE
8	Everton	EVE	https://resources.premierleague.com/premierleague/badges/t11.png	18	5	4	9	23	32	-9	19	PREMIER_LEAGUE
20	Wolverhamton Wanderers	WOL	https://resources.premierleague.com/premierleague/badges/t39.png	19	8	4	7	14	14	0	28	PREMIER_LEAGUE
\.


--
-- Data for Name: user_query_pass; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_query_pass (account_password) FROM stdin;
ure8582
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 24, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, false);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 6, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 18, true);


--
-- Name: tb_match_match_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_match_match_id_seq', 2, true);


--
-- Name: tb_player_player_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_player_player_id_seq', 142, true);


--
-- Name: tb_team_team_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_team_team_id_seq', 20, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: tb_account tb_account_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_account
    ADD CONSTRAINT tb_account_pkey PRIMARY KEY (account_id);


--
-- Name: tb_match tb_match_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_match
    ADD CONSTRAINT tb_match_pkey PRIMARY KEY (match_id);


--
-- Name: tb_player tb_player_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_player
    ADD CONSTRAINT tb_player_pkey PRIMARY KEY (player_id);


--
-- Name: tb_team tb_team_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_team
    ADD CONSTRAINT tb_team_pkey PRIMARY KEY (team_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: idx_match_id_unique; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_match_id_unique ON public.tb_match USING btree (match_id);


--
-- Name: idx_player_id_unique; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_player_id_unique ON public.tb_player USING btree (player_id);


--
-- Name: idx_player_role; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_player_role ON public.tb_player USING btree (player_role);


--
-- Name: idx_team_points; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_team_points ON public.tb_team USING btree (team_points DESC);


--
-- Name: idx_team_unique; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_team_unique ON public.tb_team USING btree (team_id, team_name, team_acronym_name);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: r_goalscore r_goalscore_gs_match_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.r_goalscore
    ADD CONSTRAINT r_goalscore_gs_match_id_fkey FOREIGN KEY (gs_match_id) REFERENCES public.tb_match(match_id);


--
-- Name: r_goalscore r_goalscore_gs_player_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.r_goalscore
    ADD CONSTRAINT r_goalscore_gs_player_id_fkey FOREIGN KEY (gs_player_id) REFERENCES public.tb_player(player_id);


--
-- Name: r_owngoal r_owngoal_og_match_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.r_owngoal
    ADD CONSTRAINT r_owngoal_og_match_id_fkey FOREIGN KEY (og_match_id) REFERENCES public.tb_match(match_id);


--
-- Name: r_owngoal r_owngoal_og_player_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.r_owngoal
    ADD CONSTRAINT r_owngoal_og_player_id_fkey FOREIGN KEY (og_player_id) REFERENCES public.tb_player(player_id);


--
-- Name: r_redcard r_redcard_rc_match_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.r_redcard
    ADD CONSTRAINT r_redcard_rc_match_id_fkey FOREIGN KEY (rc_match_id) REFERENCES public.tb_match(match_id);


--
-- Name: r_redcard r_redcard_rc_player_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.r_redcard
    ADD CONSTRAINT r_redcard_rc_player_id_fkey FOREIGN KEY (rc_player_id) REFERENCES public.tb_player(player_id);


--
-- Name: r_yellowcard r_yellowcard_yc_match_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.r_yellowcard
    ADD CONSTRAINT r_yellowcard_yc_match_id_fkey FOREIGN KEY (yc_match_id) REFERENCES public.tb_match(match_id);


--
-- Name: r_yellowcard r_yellowcard_yc_player_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.r_yellowcard
    ADD CONSTRAINT r_yellowcard_yc_player_id_fkey FOREIGN KEY (yc_player_id) REFERENCES public.tb_player(player_id);


--
-- Name: tb_match tb_match_match_enemy_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_match
    ADD CONSTRAINT tb_match_match_enemy_id_fkey FOREIGN KEY (match_enemy_id) REFERENCES public.tb_team(team_id);


--
-- PostgreSQL database dump complete
--

