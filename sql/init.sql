DO
$do$
BEGIN
IF NOT EXISTS (select 1 from pg_database where datname = 'n0blog_dev')
THEN
 CREATE DATABASE "n0blog_dev";
END IF;
IF NOT EXISTS (select 1 from pg_database where datname = 'n0blog_test')
THEN
 CREATE DATABASE "n0blog_test";
END IF;
IF NOT EXISTS (select 1 from pg_database where datname = 'n0blog')
THEN
 CREATE DATABASE "n0blog";
END IF;
END
$do$;
GRANT ALL PRIVILEGES ON DATABASE n0blog_dev TO n0blog;
GRANT ALL PRIVILEGES ON DATABASE n0blog_test TO n0blog;
GRANT ALL PRIVILEGES ON DATABASE n0blog TO n0blog;
