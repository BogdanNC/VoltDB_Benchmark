
CREATE TABLE female_document_ids (
    id BIGINT PRIMARY KEY  
);
CREATE TABLE word_count_docs (
    id_word INTEGER PRIMARY KEY,     
    wordCountDocs INTEGER 
);


INSERT INTO female_document_ids (id)
SELECT d.id AS id
FROM documents d
INNER JOIN documents_authors da ON d.id = da.id_document
INNER JOIN authors a ON da.id_author = a.id
INNER JOIN genders g ON a.id_gender = g.id
WHERE g.type = 'male'  -- Replace 'female' with the actual gender you want to filter by
    AND d.document_date BETWEEN '2015-09-17 00:00:00' AND '2015-09-18 00:00:00';

INSERT INTO word_count_docs (id_word, wordCountDocs)
SELECT v.id_word AS id_word, COUNT(DISTINCT v.id_document) AS wordCountDocs
FROM vocabulary v 
INNER JOIN female_document_ids fdi ON v.id_document = fdi.id
GROUP BY v.id_word;


SELECT q2.id AS id , SUM(q2.tfidf) AS stfidf
FROM (
    SELECT d.id as id, w.word AS word,
           (v.tf * (1 + LOG((SELECT COUNT(id) FROM female_document_ids) / q_wcd.wordCountDocs)) * (1.6 + 1)) AS tfidf
    FROM documents d
    INNER JOIN vocabulary v ON v.id_document = d.id
    INNER JOIN words w ON w.id = v.id_word
    INNER JOIN word_count_docs q_wcd ON q_wcd.id_word = v.id_word
    WHERE w.word IN ('think', 'today', 'friday')
) q2
GROUP BY q2.id
ORDER BY stfidf DESC
LIMIT 10;

DROP TABLE female_document_ids;
DROP TABLE word_count_docs;
