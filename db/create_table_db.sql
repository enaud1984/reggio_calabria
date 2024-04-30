-- Table: public.richieste_upload
CREATE EXTENSION postgis;

DROP TABLE IF EXISTS geo_labs.richieste_upload;

CREATE TABLE IF NOT EXISTS geo_labs.richieste_upload
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

ALTER TABLE IF EXISTS geo_labs.richieste_upload
    OWNER to postgres;

-- Table: geo_labs.model_execution

-- DROP TABLE IF EXISTS geo_labs.model_execution;

CREATE TABLE IF NOT EXISTS geo_labs.model_execution
(
    "ID_EXECUTION" serial NOT NULL,
    "DATE_EXECUTION" timestamp without time zone,
    "STATUS" character varying COLLATE pg_catalog."default",
    "GROUP_ID" character varying COLLATE pg_catalog."default" NOT NULL,
    "FK_MODEL" integer NOT NULL,
    "FK_SHAPE" integer NOT NULL,
    "PARAMS" json,
    "MAPPING_OUTPUT" json,
    "RESULTS" json,
    CONSTRAINT model_execution_pkey PRIMARY KEY ("ID_EXECUTION")
)
;
-- Table: geo_labs.models

-- DROP TABLE IF EXISTS geo_labs.models;

CREATE TABLE IF NOT EXISTS geo_labs.models
(
    "ID_MODEL" serial NOT NULL,
    "DATE_MODEL" timestamp without time zone,
    "STATUS" character varying COLLATE pg_catalog."default",
    "GROUP_ID" character varying COLLATE pg_catalog."default" NOT NULL,
    "CODE" character varying COLLATE pg_catalog."default" NOT NULL,
    "PARAMS" json,
    "LIBRARY" boolean NOT NULL,
    CONSTRAINT models_pkey PRIMARY KEY ("ID_MODEL")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS geo_labs.models
    OWNER to postgres;


-- Table: geo_labs.richieste_load

-- DROP TABLE IF EXISTS geo_labs.richieste_load;

CREATE TABLE IF NOT EXISTS geo_labs.richieste_load
(
    "ID_SHAPE" integer NOT NULL DEFAULT nextval('geo_labs."richieste_load_ID_SHAPE_seq"'::regclass),
    "DATE_LOAD" timestamp without time zone,
    "STATUS" character varying COLLATE pg_catalog."default",
    "GROUP_ID" character varying COLLATE pg_catalog."default" NOT NULL,
    "REQUEST" json,
    CONSTRAINT richieste_load_pkey PRIMARY KEY ("ID_SHAPE")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS geo_labs.richieste_load
    OWNER to postgres;


ALTER TABLE IF EXISTS geo_labs.model_execution
    ADD CONSTRAINT fk_model_id FOREIGN KEY ("FK_MODEL")
    REFERENCES geo_labs.models ("ID_MODEL") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_fk_model_id
    ON geo_labs.model_execution("FK_MODEL");


ALTER TABLE IF EXISTS geo_labs.model_execution
    ADD CONSTRAINT fk_shape_upload FOREIGN KEY ("FK_SHAPE")
    REFERENCES geo_labs.richieste_upload ("ID_SHAPE") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_fk_shape_upload
    ON geo_labs.model_execution("FK_SHAPE");