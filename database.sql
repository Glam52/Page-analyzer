create table urls
(
    id         serial
        primary key,
    name       varchar(255) not null,
    created_at timestamp default CURRENT_TIMESTAMP
);

alter table urls
    owner to postgres;

CREATE TABLE url_checks (
    id SERIAL PRIMARY KEY,
    url_id INTEGER NOT NULL,
    status_code INTEGER,
    h1 TEXT,
    title TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (url_id) REFERENCES urls (id)
);
