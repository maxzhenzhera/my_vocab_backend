BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 6eb0e12bd8be

CREATE TABLE users (
    id BIGSERIAL NOT NULL,
    email VARCHAR(256) NOT NULL,
    hashed_password VARCHAR(128) NOT NULL,
    password_salt VARCHAR(128) NOT NULL,
    email_confirmation_link UUID DEFAULT uuid_generate_v4() NOT NULL,
    is_active BOOLEAN DEFAULT true NOT NULL,
    is_email_confirmed BOOLEAN DEFAULT false NOT NULL,
    is_superuser BOOLEAN DEFAULT false NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    email_confirmed_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_users_email ON users (email);

CREATE TABLE oauth_connections (
    user_id BIGINT NOT NULL,
    google_id VARCHAR(64),
    PRIMARY KEY (user_id),
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE,
    UNIQUE (google_id)
);

CREATE TABLE refresh_sessions (
    refresh_token UUID DEFAULT uuid_generate_v4() NOT NULL,
    ip_address INET NOT NULL,
    user_agent VARCHAR(256) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    expires_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    user_id BIGINT NOT NULL,
    PRIMARY KEY (refresh_token),
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE tags (
    id BIGSERIAL NOT NULL,
    tag VARCHAR(64) NOT NULL,
    description VARCHAR(256),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    user_id BIGINT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TYPE language AS ENUM ('ARABIC', 'BRAZILIAN_PORTUGUESE', 'ENGLISH_UK', 'ENGLISH_US', 'FRENCH', 'GERMAN', 'HINDI', 'ITALIAN', 'JAPANESE', 'KOREAN', 'RUSSIAN', 'SPANISH', 'TURKISH');

CREATE TABLE vocabs (
    id BIGSERIAL NOT NULL,
    title VARCHAR NOT NULL,
    description VARCHAR(512),
    language language,
    is_favourite BOOLEAN DEFAULT false NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    user_id BIGINT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE vocab_tags_associations (
    vocab_id BIGINT NOT NULL,
    tag_id BIGINT NOT NULL,
    PRIMARY KEY (vocab_id, tag_id),
    FOREIGN KEY(tag_id) REFERENCES tags (id) ON DELETE CASCADE,
    FOREIGN KEY(vocab_id) REFERENCES vocabs (id) ON DELETE CASCADE
);

CREATE TABLE words (
    id BIGSERIAL NOT NULL,
    word VARCHAR(256) NOT NULL,
    is_learned BOOLEAN DEFAULT false NOT NULL,
    is_marked BOOLEAN DEFAULT false NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    vocab_id BIGINT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(vocab_id) REFERENCES vocabs (id) ON DELETE CASCADE
);

INSERT INTO alembic_version (version_num) VALUES ('6eb0e12bd8be') RETURNING alembic_version.version_num;

COMMIT;

