create table league
(
    n4_id            integer generated by default as identity
        primary key,
    str_name         varchar(50),
    str_host         varchar(50),
    str_type         varchar(50),
    str_acronym_name varchar(50),
    str_logo_link    varchar(200)
);

alter table league
    owner to pldjango;

INSERT INTO public.league (str_name, str_host, str_type, str_acronym_name, str_logo_link) VALUES ('Premiere League', 'FA', 'LEAGUE', 'EPL', 'https://pl-aws-s3.s3.ap-southeast-1.amazonaws.com/epl.png');
INSERT INTO public.league (str_name, str_host, str_type, str_acronym_name, str_logo_link) VALUES ('FA Cup', 'FA', 'CUP', 'FA', 'https://pl-aws-s3.s3.ap-southeast-1.amazonaws.com/fa.png');
INSERT INTO public.league (str_name, str_host, str_type, str_acronym_name, str_logo_link) VALUES ('Champion League', 'UEFA', 'CUP', 'UCL', 'https://pl-aws-s3.s3.ap-southeast-1.amazonaws.com/ucl.png');
INSERT INTO public.league (str_name, str_host, str_type, str_acronym_name, str_logo_link) VALUES ('Conference League', 'UEFA', 'CUP', 'UECL', 'https://pl-aws-s3.s3.ap-southeast-1.amazonaws.com/uecl.png');
INSERT INTO public.league (str_name, str_host, str_type, str_acronym_name, str_logo_link) VALUES ('Europa League', 'UEFA', 'CUP', 'UEL', 'https://pl-aws-s3.s3.ap-southeast-1.amazonaws.com/uel.png');
INSERT INTO public.league (str_name, str_host, str_type, str_acronym_name, str_logo_link) VALUES ('Carabao Cup', 'FA', 'CUP', 'EFL', 'https://pl-aws-s3.s3.ap-southeast-1.amazonaws.com/efl.png');
INSERT INTO public.league (str_name, str_host, str_type, str_acronym_name, str_logo_link) VALUES ('Club World Cup', 'Fifa', 'CUP', 'CWL', 'https://pl-aws-s3.s3.ap-southeast-1.amazonaws.com/fcwc.png');
