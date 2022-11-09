---
--- Sample table for saving sFTP users on a postgreSQL table.
---
DROP TABLE IF EXISTS public.ftpusers;
CREATE TABLE public.ftpusers
(
  userid uuid NOT NULL DEFAULT uuid_generate_v4(),
  username character varying(150) NOT NULL,
  password character varying(128) NOT NULL,
  name character varying NOT NULL DEFAULT 'John Doe'::character varying,
  last_login timestamp with time zone,
  last_ip character varying(20),
  tenant character varying(60),
  date_joined timestamp with time zone NOT NULL DEFAULT now(),
  is_active boolean NOT NULL DEFAULT true,
  CONSTRAINT pk_public_ftpusers_pkey PRIMARY KEY (userid)
)
WITH (
  OIDS=FALSE
);

--- sample users:
-- sample password is = 12345678
--- First has access to root folder
INSERT INTO public.ftpusers(username, password, name, tenant) VALUES ('jesuslara', 'pbkdf2_sha256$80000$07eb1dfa1102$gf5bifaJpu9O6IpUKT3GlCP+1VnMQ8xzzPKG/p9y8wY=', 'Jesus Lara', '');
--- Second one has access to a child folder called "docs"
INSERT INTO public.ftpusers(username, password, name, tenant) VALUES ('Tenant User', 'pbkdf2_sha256$80000$07eb1dfa1102$gf5bifaJpu9O6IpUKT3GlCP+1VnMQ8xzzPKG/p9y8wY=', 'Test Tenant', 'docs');
