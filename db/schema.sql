-- Esquema de la base "muweb" (v1). Ver docs/v1-db.md.
-- Aplicar como muweb_app:  psql "$DATABASE_URL" -f db/schema.sql

CREATE TABLE IF NOT EXISTS admin_user (
    id            serial PRIMARY KEY,
    username      text NOT NULL UNIQUE,
    password_hash text NOT NULL,
    created_at    timestamptz NOT NULL DEFAULT now(),
    last_login    timestamptz
);

CREATE TABLE IF NOT EXISTS news (
    id           serial PRIMARY KEY,
    slug         text NOT NULL UNIQUE,
    title        text NOT NULL,
    excerpt      text NOT NULL DEFAULT '',
    body_md      text NOT NULL DEFAULT '',
    tag          text NOT NULL DEFAULT '',
    published_at timestamptz NOT NULL DEFAULT now(),
    created_at   timestamptz NOT NULL DEFAULT now(),
    updated_at   timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS news_published_at_idx ON news (published_at DESC);

CREATE TABLE IF NOT EXISTS download (
    id         serial PRIMARY KEY,
    key        text NOT NULL UNIQUE,
    name       text NOT NULL,
    kind       text NOT NULL DEFAULT '',
    version    text NOT NULL DEFAULT '',
    size_bytes bigint,
    file       text,
    url        text,
    sha256     text,
    note       text NOT NULL DEFAULT '',
    available  boolean NOT NULL DEFAULT false,
    sort_order integer NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS page (
    id      serial PRIMARY KEY,
    slug    text NOT NULL UNIQUE,
    title   text NOT NULL DEFAULT '',
    body_md text NOT NULL DEFAULT '',
    visible boolean NOT NULL DEFAULT true
);

CREATE TABLE IF NOT EXISTS site_setting (
    key   text PRIMARY KEY,
    value jsonb NOT NULL
);

-- Registros hechos desde la web. Nunca guarda la contraseña.
CREATE TABLE IF NOT EXISTS web_registration (
    id         serial PRIMARY KEY,
    login_name text NOT NULL,
    email      text,
    ip         inet,
    created_at timestamptz NOT NULL DEFAULT now(),
    status     text NOT NULL DEFAULT 'created'
);
