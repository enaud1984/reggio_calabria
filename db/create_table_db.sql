-- Table: public.richieste_upload
CREATE EXTENSION postgis;
DROP TABLE IF EXISTS public.richieste_upload;

CREATE TABLE IF NOT EXISTS public.richieste_upload
(
    "ID_SHAPE" serial,
    "SHAPEFILE" character varying(2048) COLLATE pg_catalog."default",
    "DATE_UPLOAD" timestamp without time zone,
    "STATUS" character varying(256) COLLATE pg_catalog."default",
    "GROUP_ID" character varying(256) COLLATE pg_catalog."default",
    "SRID" integer DEFAULT 0,
    "PATH_SHAPEFILE" character varying(2048) COLLATE pg_catalog."default",
    "MD5" character varying(256) COLLATE pg_catalog."default",
    "USERFILE" character varying(2048)[],
    "RESPONSE" json,
    CONSTRAINT richieste_upload_pkey PRIMARY KEY ("ID_SHAPE")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.richieste_upload
    OWNER to postgres;