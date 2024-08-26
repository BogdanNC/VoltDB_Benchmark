-- Creating the dimension tables

CREATE TABLE document_dimension (
    id_document BIGINT PRIMARY KEY,
    raw_text VARCHAR,
    clean_text VARCHAR,
    lemma_text VARCHAR
);

CREATE TABLE time_dimension (
    id_time INTEGER PRIMARY KEY,
    minute TINYINT,
    hour TINYINT,
    day TINYINT,
    month TINYINT,
    year TINYINT,
    full_date TIMESTAMP
);

CREATE TABLE author_dimension (
    id_author BIGINT PRIMARY KEY,
    firstname VARCHAR(3),
    lastname VARCHAR(3),
    gender VARCHAR(8),
    age VARCHAR(4)
);

CREATE TABLE location_dimension (
    id_location SMALLINT PRIMARY KEY,
    X SMALLINT,
    Y SMALLINT
);

CREATE TABLE word_dimension (
    id_word INTEGER PRIMARY KEY,
    word VARCHAR
);

-- Creating the fact table

CREATE TABLE document_facts (
    id_document BIGINT,
    id_author BIGINT,
    id_time INTEGER,
    id_location INTEGER,
    id_word INTEGER,
    word_count INTEGER,
    tf FLOAT,
    PRIMARY KEY(id_document, id_author, id_time, id_location, id_word),
    FOREIGN KEY(id_document) REFERENCES document_dimension(id_document),
    FOREIGN KEY(id_author) REFERENCES author_dimension(id_author),
    FOREIGN KEY(id_time) REFERENCES time_dimension(id_time),
    FOREIGN KEY(id_location) REFERENCES location_dimension(id_location),
    FOREIGN KEY(id_word) REFERENCES word_dimension(id_word)
);
