CREATE TABLE public.clients
(
    "Id" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "email" character varying(128) NOT NULL,
    "password" character varying(1024) NOT NULL,
    CONSTRAINT clients_pkey PRIMARY KEY ("Id"),
    CONSTRAINT "email" UNIQUE ("email")
);