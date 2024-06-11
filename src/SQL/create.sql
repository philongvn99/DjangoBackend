create table player
(
    n4_id           serial
        primary key,
    str_name        varchar(50)                     not null,
    str_full_name   varchar(50)                     not null,
    str_avatar_link varchar(256)                    not null,
    str_nationality varchar(30)                     not null,
    dt_birthday     date default '2020-01-01'::date not null,
    is_right_foot   boolean                         not null,
    n4_kit_number   integer                         not null,
    n4_height       integer                         not null,
    str_role        player_role,
    n4_salary       integer,
    str_status      player_status
);
comment on column player.n4_height is 'positive';
comment on column player.n4_salary is 'positive';
alter table player owner topldjango;
create index idx_player_role on player (str_role);


create table league (
    n4_id    SERIAL      PRIMARY KEY,
    str_name varchar(50) not null,
    str_host varchar(50) not null,
    str_type league_type
);
alter table league owner to pldjango;

create table match
    n4_id           SERIAL     primary key,
    n4_enemy_id    integer     not null   references team,
    n4_league_id   integer     not null,
    str_stadium    varchar(50) not null,
    is_home        boolean     not null,
    n4_home_score  integer     not null,
    n4_enemy_score integer     not null,
    dt_match_day   date        not null,
    str_lineup     varchar(5),
    str_referee    varchar(50),
    str_round      round_type
);
alter table match owner to pldjango;

create table match_event
    n4_id            SERIAL     primary key,
    n4_player_id    integer     references player,
    n4_match_id     integer     references match,
    n4_minute       integer     not null,
    str_half        match_part,
    str_type        event_type
);
alter table match_event owner to pldjango;

create table team (
    n4_id            SERIAL     primary key,
    str_name         varchar(50),
    str_acronym_name varchar(50),
    str_logo_link    varchar(256),
    str_location     varchar(50)
);
alter table team owner to pldjango;
create unique index idx_team_unique on team (str_name);

create table team_attendance
    n4_id            SERIAL     primary key,
    n4_team_id   integer,
    n4_league_id integer            not null,
    n4_season    integer default 24 not null,
    n4_play      integer default 0  not null,
    n4_win       integer default 0  not null,
    n4_draw      integer default 0  not null,
    n4_lost      integer default 0  not null,
    n4_score     integer default 0  not null,
    n4_conceded  integer default 0  not null,
    n4_banned    integer default 0  not null
);
alter table team_attendance owner topldjango;
create unique index idx_team_attendance_unique on team_attendance (n4_team_id, n4_league_id, n4_season);