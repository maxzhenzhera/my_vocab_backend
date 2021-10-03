BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 4ba0d66e3838

CREATE TABLE users (
    id BIGSERIAL NOT NULL, 
    email VARCHAR NOT NULL, 
    hashed_password VARCHAR NOT NULL, 
    password_salt VARCHAR NOT NULL, 
    email_confirmation_link UUID NOT NULL, 
    is_active BOOLEAN NOT NULL, 
    is_email_confirmed BOOLEAN NOT NULL, 
    is_superuser BOOLEAN NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL, 
    email_confirmed_at TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_users_email ON users (email);

CREATE TABLE refresh_sessions (
    id BIGSERIAL NOT NULL, 
    refresh_token VARCHAR NOT NULL, 
    ip_address INET NOT NULL, 
    user_agent VARCHAR NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP), 
    expires_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    user_id BIGINT NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE tags (
    id BIGSERIAL NOT NULL, 
    title VARCHAR NOT NULL, 
    description VARCHAR, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP), 
    user_id BIGINT NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TYPE language AS ENUM ('ARABIC', 'BRAZILIAN_PORTUGUESE', 'ENGLISH_UK', 'ENGLISH_US', 'FRENCH', 'GERMAN', 'HINDI', 'ITALIAN', 'JAPANESE', 'KOREAN', 'RUSSIAN', 'SPANISH', 'TURKISH');

CREATE TABLE vocabs (
    id BIGSERIAL NOT NULL, 
    title VARCHAR NOT NULL, 
    description VARCHAR, 
    language language, 
    is_favourite BOOLEAN, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP), 
    user_id BIGINT NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE vocab_tags_associations (
    vocab_id BIGINT NOT NULL, 
    tag_id BIGINT NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP), 
    PRIMARY KEY (vocab_id, tag_id), 
    FOREIGN KEY(tag_id) REFERENCES tags (id) ON DELETE CASCADE, 
    FOREIGN KEY(vocab_id) REFERENCES vocabs (id) ON DELETE CASCADE
);

CREATE TABLE words (
    id BIGSERIAL NOT NULL, 
    word VARCHAR NOT NULL, 
    is_learned BOOLEAN, 
    is_marked BOOLEAN, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP), 
    vocab_id BIGINT NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(vocab_id) REFERENCES vocabs (id) ON DELETE CASCADE
);

INSERT INTO alembic_version (version_num) VALUES ('4ba0d66e3838') RETURNING alembic_version.version_num;

COMMIT;

