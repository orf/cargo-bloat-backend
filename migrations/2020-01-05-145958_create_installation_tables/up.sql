CREATE TABLE installs (
    id SERIAL PRIMARY KEY,
    installation_id integer NOT NULL ,
    repo text NOT NULL
);

CREATE INDEX installed_repo_idx ON installs(repo);