-- SQL file for Q1 male
CREATE TABLE doc_lengths (
    id BIGINT PRIMARY KEY,      
    docLen INTEGER   
);
CREATE TABLE avg_doclen_and_total_ids (
    avrage DECIMAL,
    total_ids INTEGER
);
CREATE TABLE no_word_docs (
    id_word INTEGER PRIMARY KEY,
    noDocWords BIGINT        
);


INSERT INTO doc_lengths (id, docLen)
SELECT f.id_document AS id , SUM(word_count) AS docLen
FROM document_facts f
INNER JOIN author_dimension ad on ad.id_author = f.id_author
INNER JOIN location_dimension ld ON ld.id_location = f.id_location
WHERE gender = 'male'
    AND ld.X BETWEEN 20 AND 40
    AND ld.Y BETWEEN -100 AND 100
GROUP BY f.id_document;

INSERT INTO avg_doclen_and_total_ids (avrage, total_ids)
SELECT AVG(docLen) AS avrage, COUNT(ID) AS total_ids FROM doc_lengths;

INSERT INTO no_word_docs (id_word, noDocWords)
SELECT f.id_word AS id_word, COUNT (DISTINCT f.id_document) AS noDocWords
FROM document_facts f
INNER JOIN author_dimension ad on ad.id_author = f.id_author
INNER JOIN location_dimension ld ON ld.id_location = f.id_location
WHERE gender = 'male'
    AND ld.X BETWEEN 20 AND 40
    AND ld.Y BETWEEN -100 AND 100
GROUP BY f.id_word;

SELECT q2.id_document, SUM (q2.okapi) AS sokapi
FROM (
    SELECT f.id_document, ( (1 + LOG(al.total_ids / ndw.noDocWords )) * (1.6 + 1) *
                (f.tf / (f.tf + 1.6 * (1 - 0.75 + 0.75 * dl.docLen / al.avrage)))) AS okapi
    FROM document_facts f
    INNER JOIN word_dimension wd ON wd.id_word = f.id_word
    INNER JOIN author_dimension ad ON ad.id_author = f.id_author
    INNER JOIN location_dimension ld ON ld.id_location = f.id_location
    INNER JOIN doc_lengths dl ON dl.id = f.id_document
    INNER JOIN no_word_docs ndw ON ndw.id_word = f.id_word
    CROSS JOIN avg_doclen_and_total_ids al 
    WHERE
        ad.gender = 'male'
        AND ld.X BETWEEN 20 AND 40
        AND ld.Y BETWEEN -100 AND 100
        and wd.word IN ('think', 'today')
) q2 
GROUP BY q2.id_document
ORDER BY sokapi DESC, 1
LIMIT 10;

DROP TABLE doc_lengths;
DROP TABLE avg_doclen_and_total_ids;
DROP TABLE no_word_docs;
