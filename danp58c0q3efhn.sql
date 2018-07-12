-- Adminer 4.6.3-dev PostgreSQL dump

\connect "danp58c0q3efhn";

DROP TABLE IF EXISTS "check_in_list";
CREATE TABLE "public"."check_in_list" (
    "checker_id" integer NOT NULL,
    "check_zipcode" integer NOT NULL
) WITH (oids = false);


DROP TABLE IF EXISTS "comments";
CREATE TABLE "public"."comments" (
    "comment" character varying NOT NULL,
    "users_id" integer,
    "zips_id" integer,
    CONSTRAINT "comments_users_id_fkey" FOREIGN KEY (users_id) REFERENCES users(id) NOT DEFERRABLE,
    CONSTRAINT "comments_zips_id_fkey" FOREIGN KEY (zips_id) REFERENCES zips(id) NOT DEFERRABLE
) WITH (oids = false);


DROP TABLE IF EXISTS "users";
DROP SEQUENCE IF EXISTS users_id_seq;
CREATE SEQUENCE users_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."users" (
    "id" integer DEFAULT nextval('users_id_seq') NOT NULL,
    "username" character varying,
    "password" character varying NOT NULL,
    CONSTRAINT "users_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "users_username_key" UNIQUE ("username")
) WITH (oids = false);


DROP TABLE IF EXISTS "zips";
DROP SEQUENCE IF EXISTS zips_id_seq;
CREATE SEQUENCE zips_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."zips" (
    "zipcode" character varying,
    "city" character varying NOT NULL,
    "state" character varying NOT NULL,
    "lat" double precision NOT NULL,
    "long" double precision NOT NULL,
    "population" integer NOT NULL,
    "id" integer DEFAULT nextval('zips_id_seq') NOT NULL,
    "check_in" integer,
    CONSTRAINT "zips_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "zips_zipcode_key" UNIQUE ("zipcode")
) WITH (oids = false);


-- 2018-07-12 15:09:22.331272+00
