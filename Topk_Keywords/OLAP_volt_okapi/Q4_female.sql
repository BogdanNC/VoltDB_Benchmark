-- SQL file for Q1 female
CREATE TABLE doc_lengths (
    id BIGINT PRIMARY KEY,      
    docLen INTEGER   
);

INSERT INTO doc_lengths (id, docLen)
SELECT f.id_document AS id , SUM(word_count) AS docLen
FROM document_facts f
INNER JOIN author_dimension ad on ad.id_author = f.id_author
INNER JOIN location_dimension ld on ld.id_location = f.id_location
INNER JOIN time_dimension td on td.id_time = f.id_time
WHERE gender = 'female'
    AND td.full_date BETWEEN '2015-09-17 00:00:00' AND '2015-09-18 00:00:00'
    AND ld.X BETWEEN 20 AND 40
    AND ld.Y BETWEEN -100 AND 100
GROUP BY f.id_document;

CREATE TABLE avg_doclen (
    avrage DECIMAL
);

INSERT INTO avg_doclen (avrage)
SELECT AVG(docLen) FROM doc_lengths;

SELECT q2.word, q2.okapi
FROM (
    SELECT wd.word, (1 + LOG((SELECT COUNT(id) FROM doc_lengths) / COUNT(DISTINCT f.id_document))) * (1.6 + 1) *
                SUM(f.tf / (f.tf + 1.6 * (1 - 0.75 + 0.75 * dl.docLen / al.avrage))) AS okapi
    FROM document_facts f
    INNER JOIN author_dimension ad ON ad.id_author = f.id_author
    INNER JOIN word_dimension wd ON wd.id_word = f.id_word
    INNER JOIN location_dimension ld on ld.id_location = f.id_location
    INNER JOIN time_dimension td on td.id_time = f.id_time
    INNER JOIN doc_lengths dl ON dl.id = f.id_document
    CROSS JOIN avg_doclen al 
    WHERE
        ad.gender = 'female'
        AND td.full_date BETWEEN '2015-09-17 00:00:00' AND '2015-09-18 00:00:00'
        AND ld.X BETWEEN 20 AND 40
        AND ld.Y BETWEEN -100 AND 100
    GROUP BY wd.word
) q2 
ORDER BY q2.okapi DESC
LIMIT 10;

DROP TABLE doc_lengths;
DROP TABLE avg_doclen;
