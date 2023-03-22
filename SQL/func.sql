DROP TYPE IF EXISTS infoType CASCADE;
DROP FUNCTION update_league_table(integer[],integer[],integer[],integer);


CREATE TYPE infoType AS (
	"id" int,
	"name" varchar(256),
	"full_name" varchar(256),
	"avatar_link" varchar(256),
	"nationality" varchar(30),
	"birthday" date,
	"right_foot" bool,
	"kit_number" int,
	"height" int,
	"role" roles,
	"salary" int,
	"status" player_statuses
  );

CREATE OR REPLACE FUNCTION get_player_by_id("p_id" int)
	RETURNS SETOF infoType
	LANGUAGE plpgsql AS
	$func$
		BEGIN
			RETURN QUERY
				SELECT *
				FROM  tb_player
				WHERE player_id = "p_id";
		END
	$func$;

CREATE OR REPLACE FUNCTION get_all_teams("season" smallint DEFAULT 2023)
	RETURNS SETOF tb_team
	LANGUAGE plpgsql AS
	$func$
		BEGIN
			RETURN QUERY
				SELECT * FROM tb_team 
					WHERE team_season = "season"

					ORDER BY 	team_points DESC, 
								team_goal_difference DESC,
								team_goal_for DESC,
								team_goal_against ASC,
								team_name ASC;
		END
	$func$;

CREATE OR REPLACE FUNCTION  update_league_table(
		idList varchar[],
		gsList int[],
		gcList int[],
		nMatch int,
		league leagues,
		season int
	)
	RETURNS TABLE (
		tname varchar(256),
		played_game int,
		win_game int,
		drawn_game int,
		lost_game int,
		goal_for int,
		goal_against int,
		goal_difference int,
		points int
	)
  	LANGUAGE plpgsql AS
	$func$
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
			EXECUTE FORMAT(
						'UPDATE tb_group_stage
							SET 
								%1$s = %1$s + 1,
								team_played_game = team_played_game + 1,
								team_goal_for = team_goal_for + %3$s,
								team_goal_against = team_goal_against + %4$s,
								team_goal_difference = team_goal_difference + %3$s - %4$s,
								team_points = team_points + %2$s
							WHERE team_id = %5$s AND team_season = %6$s AND team_league = %7$s', 
						resType, 
						addPts, 
						gsList[i], 
						gcList[i], 
						idList[i],
						season,
						league
					);
		END LOOP;
		------------------------
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
	$func$;

CREATE OR REPLACE FUNCTION  clear_league_table()
	RETURNS TABLE (
			tname varchar(256),
			played_game int,
			win_game int,
			drawn_game int,
			lost_game int,
			goal_for int,
			goal_against int,
			goal_difference int,
			points int
		)
  	LANGUAGE plpgsql AS
	$func$
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
		---------------------------------
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
	$func$;


CREATE OR REPLACE FUNCTION authenticate_user(user_name VARCHAR(256), user_password VARCHAR(256))
	RETURNS user_return_info
	LANGUAGE plpgsql AS
	$func$
	DECLARE 
		user_info user_return_info DEFAULT NULL;
	BEGIN
		SELECT account_username AS username, account_email AS email, account_phone AS phone, account_name AS "name"
			INTO user_info
			FROM tb_account
			WHERE ((account_username = user_name) OR (account_phone = user_name) OR (account_phone = user_name)) AND (account_password = user_password);
		RETURN user_info;
	END;
	$func$

CREATE OR REPLACE FUNCTION get_user_by_username(user_name VARCHAR(256))
	RETURNS RECORD
	LANGUAGE plpgsql AS
	$func$
	DECLARE
		user_info user_return_info DEFAULT NULL;
	BEGIN
		SELECT account_username AS username, account_email AS email, account_phone AS phone, account_name AS "name"
			FROM tb_account
			INTO user_info
			WHERE (account_username = user_name) OR (account_phone = user_name) OR (account_phone = user_name));
	END;
	$func$

INSERT INTO "tb_team"("team_name", "team_acronym_name", "team_logo_link", "team_league") VALUES 
('Arsenal', 'ARS', 'https://resources.premierleague.com/premierleague/badges/t3.png',  'PREMIER_LEAGUE'),
('Aston Villa', 'AVL', 'https://resources.premierleague.com/premierleague/badges/t7.png',  'PREMIER_LEAGUE'),
('Brenford', 'BRE', 'https://resources.premierleague.com/premierleague/badges/t94.png',  'PREMIER_LEAGUE'),
('Bournemouth', 'BOU', 'https://resources.premierleague.com/premierleague/badges/t91.png',  'PREMIER_LEAGUE'),
('Brighton and Hove Albion', 'BHA', 'https://resources.premierleague.com/premierleague/badges/t36.png',  'PREMIER_LEAGUE'),
('Chelsea', 'CHE', 'https://resources.premierleague.com/premierleague/badges/t8.png',  'PREMIER_LEAGUE'),
('Crystal Palace', 'CRY', 'https://resources.premierleague.com/premierleague/badges/t31.png',  'PREMIER_LEAGUE'),
('Everton', 'EVE', 'https://resources.premierleague.com/premierleague/badges/t11.png',  'PREMIER_LEAGUE'),
('Fulham', 'FUL', 'https://resources.premierleague.com/premierleague/badges/t54.png',  'PREMIER_LEAGUE'),
('Leeds United', 'LEE', 'https://resources.premierleague.com/premierleague/badges/t2.png',  'PREMIER_LEAGUE'),
('Leicester City', 'LEI', 'https://resources.premierleague.com/premierleague/badges/t13.png',  'PREMIER_LEAGUE'),
('Liverpool', 'LIV', 'https://resources.premierleague.com/premierleague/badges/t14.png',  'PREMIER_LEAGUE'),
('Manchester City', 'MCI', 'https://resources.premierleague.com/premierleague/badges/t43.png',  'PREMIER_LEAGUE'),
('Manchester United', 'MUN', 'https://resources.premierleague.com/premierleague/badges/t1.png',  'PREMIER_LEAGUE'),
('Newcastle United', 'NEW', 'https://resources.premierleague.com/premierleague/badges/t4.png',  'PREMIER_LEAGUE'),
('Nottingham Forest', 'NFO', 'https://resources.premierleague.com/premierleague/badges/t17.png',  'PREMIER_LEAGUE'),
('Southamton', 'SOU', 'https://resources.premierleague.com/premierleague/badges/t20.png',  'PREMIER_LEAGUE'),
('Tottenham Hotspur', 'TOT', 'https://resources.premierleague.com/premierleague/badges/t6.png',  'PREMIER_LEAGUE'),
('West Ham United', 'WHU', 'https://resources.premierleague.com/premierleague/badges/t21.png',  'PREMIER_LEAGUE'),
('Wolverhamton Wanderers', 'WOL', 'https://resources.premierleague.com/premierleague/badges/t39.png',  'PREMIER_LEAGUE');

UPDATE "tb_team" SET "team_id" = CONCAT(team_acronym_name, '_', (team_season-2000)::varchar(10));