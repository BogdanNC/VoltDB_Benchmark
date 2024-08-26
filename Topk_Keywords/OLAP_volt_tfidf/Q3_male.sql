
CREATE TABLE no_docs (
    id BIGINT PRIMARY KEY,         
);

INSERT INTO no_docs (id)
SELECT DISTINCT f.id_document AS id
FROM document_facts f
INNER JOIN author_dimension ad on ad.id_author = f.id_author
INNER JOIN location_dimension ld on ld.id_location = f.id_location
WHERE gender = 'male'
    AND ld.X BETWEEN 20 AND 40
    AND ld.Y BETWEEN -100 AND 100;

SELECT q2.word, q2.tfidf
FROM (
    SELECT wd.word, SUM(f.tf) * (1 + LOG((SELECT COUNT(id) FROM no_docs) / COUNT(DISTINCT f.id_document)))  AS tfidf
    FROM document_facts f
    INNER JOIN author_dimension ad ON ad.id_author = f.id_author
    INNER JOIN word_dimension wd ON wd.id_word = f.id_word
    INNER JOIN location_dimension ld on ld.id_location = f.id_location
    WHERE gender = 'male'
        AND ld.X BETWEEN 20 AND 40
        AND ld.Y BETWEEN -100 AND 100
    GROUP BY wd.word
) q2 
ORDER BY q2.tfidf DESC
LIMIT 10;

DROP TABLE no_docs;
