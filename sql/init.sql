DO
$do$
BEGIN
IF NOT EXISTS (select 1 from pg_database where datname = 'n0blog')
THEN
 CREATE DATABASE "n0blog";
 GRANT ALL PRIVILEGES ON DATABASE n0blog TO n0blog;
END IF;
END
$do$;
