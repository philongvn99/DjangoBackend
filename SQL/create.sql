-- DROP VIEWS
DROP VIEW IF EXISTS v_defenders, v_goalkeepers, v_forwards, v_midfielders CASCADE, user_return_info;

-- DROP TABLES and RELATIONS
DROP TABLE IF EXISTS r_goalscore, r_owngoal, r_yellow_card, r_red_card;
DROP TABLE IF EXISTS tb_match;
DROP TABLE IF EXISTS tb_league_table;
DROP TABLE IF EXISTS tb_player_info;

-- DROP TYPES
DROP TYPE IF EXISTS "accounttypes", "matchtypes", "roles", "player_statuses";

-- DROP INDEXES

CREATE TYPE user_return_info AS (
	"username" varchar(256),
	"email" varchar(256),
	"phone" varchar(256),
	"name" varchar(256)
);

CREATE TYPE "matchtypes" AS ENUM (
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

CREATE TYPE "roles" AS ENUM (
  'GOALKEEPER',
  'DEFENDER',
  'MIDFIELDER',
  'FORWARD'
);

CREATE TYPE "leagues" AS ENUM (
  'CHAMPIONS_LEAGUE',
  'EUROPA_LEAGUE',
  'PREMIER_LEAGUE',
  'FA_CUP',
  'CARABAO_CUP'
);

CREATE TYPE "player_statuses" AS ENUM (
  'ACTIVE',
  'LOAN',
  'LEFT'
);

CREATE TYPE "accounttypes" AS ENUM (
  'ADMIN',
  'USER',
  'GUESY'
);

CREATE TABLE "tb_player" (
  "player_id" SERIAL PRIMARY KEY,
  "player_name" varchar(256) NOT NULL,
  "player_full_name" varchar(256) NOT NULL,
  "player_avatar_link" varchar(256) NOT NULL,
  "player_nationality" varchar(30) NOT NULL,
  "player_birthday" date NOT NULL DEFAULT '01/01/2020',
  "player_right_foot" BOOLEAN NOT NULL,
  "player_kit_number" int NOT NULL,
  "player_height" int NOT NULL,
  "player_role" roles,
  "player_salary" int,
  "player_status" player_statuses
);

CREATE TABLE "tb_team" (
  "team_id" SERIAL PRIMARY KEY,
  "team_name" varchar(256),
  "team_acronym_name" varchar(256),
  "team_logo_link" varchar(256),
  "team_played_game" int NOT NULL DEFAULT 0,
  "team_win_game" int NOT NULL DEFAULT 0,
  "team_drawn_game" int NOT NULL DEFAULT 0,
  "team_lost_game" int NOT NULL DEFAULT 0,
  "team_goal_for" int NOT NULL DEFAULT 0,
  "team_goal_against" int NOT NULL DEFAULT 0,
  "team_goal_difference" int NOT NULL DEFAULT 0,
  "team_points" int NOT NULL DEFAULT 0,
  "league" leagues NOT NULL DEFAULT 'PREMIER_LEAGUE'
);

CREATE TABLE "tb_match" (
  "match_id" SERIAL PRIMARY KEY,
  "match_enemy_id" int NOT NULL,
  "match_stadium" varchar(256) NOT NULL,
  "match_home" BOOLEAN NOT NULL,
  "match_home_score" int,
  "match_enemy_score" int,
  "match_date" date,
  "match_lineup" varchar(5),
  "match_referee" varchar(256),
  "match_type" matchtypes
);

CREATE TABLE "r_goalscore" (
  "gs_player_id" int,
  "gs_match_id" int,
  "gs_minute" int
);

CREATE TABLE "r_owngoal" (
  "og_player_id" int,
  "og_match_id" int,
  "og_minute" int
);

CREATE TABLE "r_yellowcard" (
  "yc_player_id" int,
  "yc_match_id" int,
  "yc_minute" int
);

CREATE TABLE "r_redcard" (
  "rc_player_id" int,
  "rc_match_id" int,
  "rc_minute" int
);

CREATE TABLE "tb_account" (
	"account_id" varchar(256) NOT NULL PRIMARY KEY,
	"account_email" varchar(256) NOT NULL, 
	"account_username" varchar(256) NOT NULL,
	"account_phone" varchar(256) NOT NULL,
	"account_name" varchar(256) NOT NULL,
	"account_password" varchar(256) NOT NULL,
	"account_role" accounttypes NOT NULL
);

--ADD FOREIGN KEY

ALTER TABLE "tb_match" ADD FOREIGN KEY ("match_enemy_id") REFERENCES "tb_team" ("team_id");

ALTER TABLE "r_goalscore" ADD FOREIGN KEY ("gs_player_id") REFERENCES "tb_player" ("player_id");

ALTER TABLE "r_goalscore" ADD FOREIGN KEY ("gs_match_id") REFERENCES "tb_match" ("match_id");

ALTER TABLE "r_owngoal" ADD FOREIGN KEY ("og_player_id") REFERENCES "tb_player" ("player_id");

ALTER TABLE "r_owngoal" ADD FOREIGN KEY ("og_match_id") REFERENCES "tb_match" ("match_id");

ALTER TABLE "r_yellowcard" ADD FOREIGN KEY ("yc_player_id") REFERENCES "tb_player" ("player_id");

ALTER TABLE "r_yellowcard" ADD FOREIGN KEY ("yc_match_id") REFERENCES "tb_match" ("match_id");

ALTER TABLE "r_redcard" ADD FOREIGN KEY ("rc_player_id") REFERENCES "tb_player" ("player_id");

ALTER TABLE "r_redcard" ADD FOREIGN KEY ("rc_match_id") REFERENCES "tb_match" ("match_id");

-- create indexes

CREATE UNIQUE INDEX "idx_team_unique" ON "tb_team" ("team_id", "team_name", "team_acronym_name");

CREATE INDEX "idx_team_points" ON "tb_team" ("team_points" DESC);

CREATE UNIQUE INDEX "idx_match_id_unique" ON "tb_match" ("match_id");

CREATE UNIQUE INDEX "idx_player_id_unique" ON "tb_player" ("player_id");

CREATE INDEX "idx_player_role" ON "tb_player" ("player_role");

-- create comment
COMMENT ON COLUMN "tb_player"."player_height" IS 'positive';

COMMENT ON COLUMN "tb_player"."player_salary" IS 'positive';

-- create GOALKEEPERS view
CREATE OR REPLACE VIEW v_goalkeepers AS 
	SELECT player_id, player_name, player_nationality, player_birthday, player_height, player_role, player_salary, player_status
  FROM tb_player where player_role = 'GOALKEEPER';
	
-- create DEFENDERS view
CREATE OR REPLACE VIEW v_defenders AS 
	SELECT player_id, player_name, player_nationality, player_birthday, player_height, player_role, player_salary, player_status
  FROM tb_player where player_role = 'DEFENDER';
	
-- create MIDFIELDERS view
CREATE OR REPLACE VIEW v_midfielders AS 
	SELECT player_id, player_name, player_nationality, player_birthday, player_height, player_role, player_salary, player_status
  FROM tb_player where player_role = 'MIDFIELDER';
	
-- create FORWARDS view
CREATE OR REPLACE VIEW v_forwards AS 
	SELECT player_id, player_name, player_nationality, player_birthday, player_height, player_role, player_salary, player_status
  FROM tb_player where player_role = 'FORWARD';

-- create Triggers

-- ADD VALUE

----add match

----add player

INSERT INTO tb_player  (
	player_name, 
	player_full_name,
	player_avatar_link, 
	player_nationality, 
	player_birthday, 
	player_right_foot, 
	player_kit_number, 
	player_height, 
	player_role, 
	player_salary,
	player_status
)
	VALUES
		('De Gea', 			    'David de Gea Quintana', 				  'https://resources.premierleague.com/premierleague/photos/players/250x250/p51940.png',	                                        'Spain', 		  '1990-11-07', TRUE, 	1, 		192, 'GOALKEEPER', 	375, 	'ACTIVE'),
		('Dean Henderson', 	'Dean Bradley Henderson', 			  'https://resources.premierleague.com/premierleague/photos/players/250x250/p172649.png',	                                          'Endland', 		'1997-03-12', TRUE, 	26, 	188, 'GOALKEEPER', 	100, 	'ACTIVE'),
		('Maguire', 		    'Jacob Harry Maguire', 					  'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000142/Treated_Player_Profile_Thumbnail_Maguire_11626421871630.jpg',	  'Endland', 		'1993-03-05', TRUE, 	5, 		194, 'DEFENDER', 	  190, 	'ACTIVE'),
		('Lindelof', 		    'Victor Jorgen Nilsson Lindelof', 'https://resources.premierleague.com/premierleague/photos/players/250x250/p184667.png',	                                          'Sweden', 		'1994-07-17', TRUE, 	2, 		187, 'DEFENDER', 	  120, 	'ACTIVE'),
		('Varane', 			    'Raphael Xavier Varane', 				  'https://assets.manutd.com/AssetPicker/images/0/0/15/121/1014053/Player_Profile_Thumbnail_RV_metadata_removed1629814324519.jpg','France', 		'1993-04-25', TRUE, 	99,		191, 'DEFENDER', 	  172,	'ACTIVE'),
		('Bailly', 			    'Eric Bertrand Bailly', 				  'https://resources.premierleague.com/premierleague/photos/players/250x250/p197365.png',	                                        'Ivory Coast','1994-03-05', TRUE, 	3,  	187, 'DEFENDER', 	  80, 	'ACTIVE'),
		('Tuanzebe', 		    'Axel Tuanzebe', 						      'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000161/Treated_Player_Profile_Thumbnail_Tuanzebe1626424466159.jpg',	  'Congo', 		  '1997-11-14', TRUE, 	38, 	186, 'DEFENDER', 	  50, 	'ACTIVE'),
		('Phil Jones', 		  'Phil Anthony Jones', 					  'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000145/Treated_Player_Profile_Thumbnail_Jones1626423306220.jpg',	      'Endland', 		'1992-02-21', TRUE, 	4,  	185, 'DEFENDER', 	  75, 	'ACTIVE'),
		('Telles', 			    'Alex Nicolao Telles', 					  'https://assets.manutd.com/AssetPicker/images/0/0/15/55/997174/Alex_Telles_Landingpage1626421346294.jpg',	                      'Brazil', 		'1992-12-15', TRUE, 	27, 	181, 'DEFENDER', 	  93, 	'ACTIVE'),
		('Luke Shaw', 		  'Luke Paul Hoare Shaw', 				  'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000135/Treated_Player_Profile_Thumbnail_Shaw1626422466032.jpg',	      'Endland', 		'1995-07-12', FALSE, 	23, 	185, 'DEFENDER', 	  150, 	'ACTIVE'),
		('Brandon W.', 		  'Brandon Paul Brian Williams', 		'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000157/Treated_Player_Profile_Thumbnail_Williams1626356183344.jpg',	  'Endland', 		'2000-09-03', FALSE, 	33, 	172, 'DEFENDER', 	  65, 	'ACTIVE'),
		('wan Bissaka', 	  'Aaron Wan-Bissaka', 					    'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000158/Treated_Player_Profile_Thumbnail_Wans_Bissaka1626355531775.jpg','Endland', 		'1997-11-26', TRUE, 	29,  	183, 'DEFENDER', 	  90, 	'ACTIVE'),
		('Diogo Dalot', 	  'Jose Diogo Dalot Teixeira', 			'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000150/Treated_Player_Profile_Thumbnail_Dalot1626356756247.jpg',	      'Portugal', 	'1999-03-18', TRUE, 	20,  	183, 'DEFENDER', 	  54 , 	'ACTIVE'),
    ('Teden Mengi', 	  'Teden Mambuene Mengi', 			    'https://assets.manutd.com/AssetPicker/images/0/0/15/55/997254/mengi_player_grid__2_1626423846616.jpg',	                        'England', 	  '2002-04-30', TRUE, 	43,  	186, 'DEFENDER', 	  1 , 	'ACTIVE'),
		('Matic', 			    'Nemanja Matic', 						      'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000139/Treated_Player_Profile_Thumbnail_Matic1626423129191.jpg',	      'Serbia', 		'1988-08-01', FALSE, 	31,  	194, 'MIDFIELDER', 	120, 	'ACTIVE'),
		('James Garner',	  'James David Garner', 					  'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000147/Treated_Player_Profile_Thumbnail_Garner1626421974124.jpg',	    'England', 		'2001-03-13', TRUE, 	37,  	182, 'MIDFIELDER', 	19, 	'LOAN'),
		('Pogba', 			    'Paul Labile Pogba', 					    'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000137/Treated_Player_Profile_Thumbnail_Pogba1626423217888.jpg',	      'France', 		'1993-03-15', TRUE, 	6,  	191, 'MIDFIELDER', 	290, 	'ACTIVE'),
		('Van De Beek', 	  'Donny van de Beek', 					    'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000159/Treated_Player_Profile_Thumbnail_van_de_Beek1626356866391.jpg',	'Netherlands','1997-04-18', TRUE, 	34,  	184, 'MIDFIELDER', 	120, 	'ACTIVE'),
		('McTominay', 		  'Scott Francis McTominay', 				'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000138/Treated_Player_Profile_Thumbnail_McTominay1626423399235.jpg',	  'Scotland', 	'1996-12-08', TRUE, 	39,  	191, 'MIDFIELDER', 	20, 	'ACTIVE'),
		('Fred', 			      'Frederico Rodrigues de Paula Santos', 	'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000148/Treated_Player_Profile_Thumbnail_Fred1626421779442.jpg',	'Brazil', 		'1993-03-05', FALSE, 	17,  	169, 'MIDFIELDER', 	120, 	'ACTIVE'),
		('Bruno Fernandes',	'Bruno Miguel Borges Fernandes',  'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000149/Treated_Player_Profile_Thumbnail_Fernandes1626356273672.jpg',	  'Portugal', 	'1994-09-08', TRUE, 	18,  	179, 'MIDFIELDER', 	180, 	'ACTIVE'),
		('Pellistri', 		  'Facundo Pellistri', 					    'https://assets.manutd.com/AssetPicker/images/0/0/15/55/997199/Facundo_Pellistri_Landingpage1626421662586.jpg',	                'Uruguay', 		'2001-12-20', TRUE, 	28,  	175, 'MIDFIELDER', 	15,		'ACTIVE'),
		('Mata', 			      'Juan Manuel Mata Garcia',				'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000140/Treated_Player_Profile_Thumbnail_Mata_11626422203863.jpg',	    'Spain', 		  '1988-04-28', FALSE, 	8,  	170, 'MIDFIELDER', 	160, 	'ACTIVE'),
		('Andreas Pereira', 'Andreas Hugo Hoelgebaum Pereira','https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000154/Treated_Player_Profile_Thumbnail_A_Periera1626355847241.jpg',	  'Brazil', 		'1996-01-01', TRUE, 	15,  	177, 'MIDFIELDER', 	30,		'LOAN'),
		('Hannibal', 			  'Hannibal Mejbri', 				        'https://resources.premierleague.com/premierleague/photos/players/250x250/p465527.png',	                                        'Tunisia', 		'2003-01-21', TRUE, 	46, 	182, 'MIDFIELDER', 	0, 	  'ACTIVE'),
    ('Lingard', 		    'Jesse Ellis Lingard', 					  'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000143/Treated_Player_Profile_Thumbnail_Lingard1626422106800.jpg',	    'Spain', 		  '1992-12-15', TRUE, 	14,  	175, 'MIDFIELDER', 	58,		'ACTIVE'),
		('Daniel James', 	  'Daniel Owen James', 					    'https://saybongda.com/wp-content/uploads/2021/05/Daniel-James-avt-1024x773.jpg',	                                              'Wales', 		  '1997-11-10', TRUE, 	21,  	170, 'FORWARD', 	  45, 	'LEFT'),
		('Rashford', 		    'Marcus Rashford MBE', 					  'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000136/Treated_Player_Profile_Thumbnail_Rashford1626422926368.jpg',	  'Endland', 		'1997-10-31', TRUE, 	10,  	185, 'FORWARD', 	  200, 	'ACTIVE'),
		('Greenwood', 		  'Mason Will John Greenwood', 			'https://resources.premierleague.com/premierleague/photos/players/250x250/p220688.png',                                         'Endland', 		'2001-10-01', FALSE, 	11,  	181, 'FORWARD', 	  35, 	'ACTIVE'),
		('Amad Diallo', 	  'Amad Diallo', 							      'https://assets.manutd.com/AssetPicker/images/0/0/15/55/997198/Amad_Diallo_Landingpage1626421446601.jpg',	                      'Ivory Coast','2002-07-11', FALSE, 	16,  	173, 'FORWARD', 	  48, 	'ACTIVE'),
		('Sancho', 			    'Jadon Malik Sancho', 					  'https://assets.manutd.com/AssetPicker/images/0/0/15/78/1003014/Player-Profile-Thumbnail-Sancho1627370980650.jpg',	            'England', 		'2000-03-25', TRUE, 	25,  	180, 'FORWARD', 	  350, 	'ACTIVE'),
		('Martial', 		    'Anthony Jordan Martial', 				'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000141/Treated_Player_Profile_Thumbnail_Martial_11626355968632.jpg',	  'France', 		'1995-12-05', TRUE, 	9,  	181, 'FORWARD', 	  250, 	'ACTIVE'),
		('Cavani', 			    'Edinson Roberto Cavani Gomez', 	'https://assets.manutd.com/AssetPicker/images/0/0/15/55/997213/Edinson_Cavani_Landingpage1626421572829.jpg',	                  'Uruguay', 		'1987-02-14', TRUE, 	21,  	184, 'FORWARD', 	  210, 	'ACTIVE'),
    ('Ronaldo', 			  'Cristian Ronaldo dos Santos Aveiro', 				'https://resources.premierleague.com/premierleague/photos/players/250x250/p14937.png',	                            'Portugal', 	'1990-05-02', TRUE, 	7, 		185, 'FORWARD', 	  385, 	'ACTIVE'),
    ('Elanga', 			    'Anthony David Junior Elanga', 		'https://resources.premierleague.com/premierleague/photos/players/250x250/p449434.png',	                                        'Sweden', 		'2002-04-27', TRUE, 	36, 	178, 'FORWARD', 	  0, 	  'ACTIVE'),
    ('Shoretire', 			'Shola Maxwell Shoretire', 			  'https://resources.premierleague.com/premierleague/photos/players/250x250/p472464.png',	                                        'England', 		'2004-02-02', TRUE, 	47, 	171, 'FORWARD', 	  0, 	  'ACTIVE'),
    ('Tahith Chong', 		'Tahith Chong', 				          'https://assets.manutd.com/AssetPicker/images/0/0/15/66/1000151/Treated_Player_Profile_Thumbnail_Chong1626423490987.jpg',	      'Netherlands','1999-12-04', FALSE, 	44, 	185, 'FORWARD', 	  0, 	  'LOAN');



----add league

INSERT INTO tb_team (team_name, team_acronym_name, team_logo_link) VALUES 
		('Arsenal', 					'ARS', 'https://resources.premierleague.com/premierleague/badges/t3.png'),
		('Aston Villa', 				'AVL', 'https://resources.premierleague.com/premierleague/badges/t7.png'),
		('Brenford',					'BRE', 'https://resources.premierleague.com/premierleague/badges/t94.png'),
		('Brighton and Hove Albion', 	'BHA', 'https://resources.premierleague.com/premierleague/badges/t36.png'),
		('Burnley',						'BUR', 'https://resources.premierleague.com/premierleague/badges/t90.png'),
		('Chelsea', 					'CHE', 'https://resources.premierleague.com/premierleague/badges/t8.png'),
		('Crystal Palace', 				'CRY', 'https://resources.premierleague.com/premierleague/badges/t31.png'),
		('Everton', 					'EVE', 'https://resources.premierleague.com/premierleague/badges/t11.png'),
		('Leeds United', 				'LEE', 'https://resources.premierleague.com/premierleague/badges/t2.png'),
		('Leicester City', 				'LEI', 'https://resources.premierleague.com/premierleague/badges/t13.png'),
		('Liverpool', 					'LIV', 'https://resources.premierleague.com/premierleague/badges/t14.png'),
		('Manchester City', 			'MCI', 'https://resources.premierleague.com/premierleague/badges/t43.png'),
		('Manchester United',			'MUN', 'https://resources.premierleague.com/premierleague/badges/t1.png'),
		('Newcastle United', 			'NEW', 'https://resources.premierleague.com/premierleague/badges/t4.png'),
		('Norwich City', 				'NOR', 'https://resources.premierleague.com/premierleague/badges/t45.png'),
		('Southamton', 					'SOU', 'https://resources.premierleague.com/premierleague/badges/t20.png'),
		('Tottenham Hotspur', 			'TOT', 'https://resources.premierleague.com/premierleague/badges/t6.png'),
		('Watford', 					'WAT', 'https://resources.premierleague.com/premierleague/badges/t57.png'),
		('West Ham United', 			'WHU', 'https://resources.premierleague.com/premierleague/badges/t21.png'),
		('Wolverhamton Wanderers', 		'WOL', 'https://resources.premierleague.com/premierleague/badges/t39.png');
		

INSERT INTO tb_match (
	match_enemy_id, 
	match_stadium, 
	match_home
) 
	VALUES 
		(9, 'Old Trafford', TRUE), 
		(16, 'St MARRY', FALSE);


INSERT INTO tb_account (
	account_id,
	account_name,
	account_username, 
	account_email,
	account_phone,
	account_password,
	account_role
) 
  VALUES 
    ('585F072E30U', 'Phi Long 6/3', 'dr3g0ng44m', 	'long.vonguyenphi@gmail.com', '0327071985', '01886933234', 'ADMIN'),
    ('585F072E31U', 'YooNaLimmm',   'dr3g0ng44n', 	'dr3g0ng44m@gmail.com', '0327071985', 'binbin123', 'USER'),
    ('6735323825U', 'Elia249315', 	'holtby331', 	'holtby331@gmail.com', '01886933234', 'ure8582', 'USER');