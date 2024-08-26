-- Creating the dimension tables

CREATE TABLE geo_location (
    id SMALLINT PRIMARY KEY,
    X SMALLINT,
    Y SMALLINT
);

CREATE TABLE documents (
    id BIGINT PRIMARY KEY,
    id_geo_loc SMALLINT,
    raw_text VARCHAR,
    lemma_text VARCHAR,
    clean_text VARCHAR,
    document_date TIMESTAMP,
    FOREIGN KEY(id_geo_loc) REFERENCES geo_location(id)
);

CREATE TABLE genders (
    id TINYINT PRIMARY KEY,
    type VARCHAR(8)
);

CREATE TABLE authors (
    id_gender TINYINT,
    id BIGINT PRIMARY KEY,
    firstname VARCHAR(3),
    lastname VARCHAR(3),
    age SMALLINT,
    FOREIGN KEY(id_gender) REFERENCES genders(id)
);

CREATE TABLE documents_authors (
    id_author BIGINT,
    id_document BIGINT,
    PRIMARY KEY(id_author, id_document),
    FOREIGN KEY(id_author) REFERENCES authors(id),
    FOREIGN KEY(id_document) REFERENCES documents(id)
);

CREATE TABLE words (
    id INTEGER PRIMARY KEY,
    word VARCHAR
);

CREATE TABLE vocabulary (
    id_document BIGINT,
    id_word INTEGER,
    word_count INTEGER,
    tf FLOAT,
    PRIMARY KEY(id_document, id_word),
    FOREIGN KEY(id_document) REFERENCES documents(id),
    FOREIGN KEY(id_word) REFERENCES words(id)
);
