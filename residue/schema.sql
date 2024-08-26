CREATE TABLE user_data (
    id BIGINT NOT NULL,
    raw_text VARCHAR(500),
    PRIMARY KEY(id)
);

CREATE PROCEDURE SearchText AS
    SELECT id, raw_text
    FROM user_data
    WHERE raw_text LIKE '%you%';



