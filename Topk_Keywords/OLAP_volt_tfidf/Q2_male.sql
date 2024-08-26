-- SQL file for Q1 female
CREATE TABLE no_docs (
    id BIGINT PRIMARY KEY,         
);

INSERT INTO no_docs (id)
SELECT DISTINCT f.id_document AS id
FROM document_facts f
INNER JOIN author_dimension ad on ad.id_author = f.id_author
INNER JOIN time_dimension td on td.id_time = f.id_time
WHERE gender = 'male'
    AND td.full_date BETWEEN '2015-09-17 00:00:00' AND '2015-09-18 00:00:00';

SELECT q2.word, q2.tfidf
FROM (
    SELECT wd.word, SUM(f.tf) * (1 + LOG((SELECT COUNT(id) FROM no_docs) / COUNT(DISTINCT f.id_document)))  AS tfidf
    FROM document_facts f
    INNER JOIN author_dimension ad ON ad.id_author = f.id_author
    INNER JOIN word_dimension wd ON wd.id_word = f.id_word
    INNER JOIN time_dimension td on td.id_time = f.id_time
    WHERE ad.gender = 'male'
        AND td.full_date  BETWEEN '2015-09-17 00:00:00' AND '2015-09-18 00:00:00'
    GROUP BY wd.word
) q2 
ORDER BY q2.tfidf DESC
LIMIT 10;

DROP TABLE no_docs;
