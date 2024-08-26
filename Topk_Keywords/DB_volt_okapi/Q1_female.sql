CREATE TABLE doc_lengths (
    id BIGINT PRIMARY KEY,      
    docLen BIGINT   
);
CREATE TABLE female_document_ids (
    id BIGINT PRIMARY KEY  
);
CREATE TABLE word_count_docs (
    id_word INTEGER PRIMARY KEY,     
    wordCountDocs INTEGER 
);

INSERT INTO doc_lengths (id, docLen)
SELECT d.id AS id, SUM(v.word_count) AS docLen
FROM documents d
INNER JOIN vocabulary v ON v.id_document = d.id
INNER JOIN documents_authors da ON d.id = da.id_document
INNER JOIN authors a ON da.id_author = a.id
INNER JOIN genders g ON a.id_gender = g.id
WHERE g.type = 'female' -- Replace 'female' with the actual gender you want to filter by
GROUP BY d.id;


INSERT INTO female_document_ids (id)
SELECT d.id AS id
FROM documents d
INNER JOIN documents_authors da ON d.id = da.id_document
INNER JOIN authors a ON da.id_author = a.id
INNER JOIN genders g ON a.id_gender = g.id
WHERE g.type = 'female';  -- Replace 'female' with the actual gender you want to filter by


INSERT INTO word_count_docs (id_word, wordCountDocs)
SELECT v.id_word AS id_word, COUNT(DISTINCT v.id_document) AS wordCountDocs
FROM vocabulary v 
INNER JOIN female_document_ids fdi ON v.id_document = fdi.id
GROUP BY v.id_word;


SELECT q2.word, SUM(q2.okapi) AS sokapi
FROM (
    SELECT d.id as id, w.word AS word,
           (v.tf * (1 + LOG((SELECT COUNT(id) FROM female_document_ids) / q_wcd.wordCountDocs)) * (1.6 + 1)) /
           (v.tf + 1.6 * (1 - 0.75 + 0.75 * q_dl.docLen / (SELECT AVG(docLen) FROM doc_lengths))) AS okapi
    FROM documents d
    INNER JOIN vocabulary v ON v.id_document = d.id
    INNER JOIN words w ON w.id = v.id_word
    INNER JOIN doc_lengths q_dl ON q_dl.id = d.id
    INNER JOIN word_count_docs q_wcd ON q_wcd.id_word = v.id_word
) q2
GROUP BY q2.word
ORDER BY sokapi DESC
LIMIT 10;

DROP TABLE doc_lengths;
DROP TABLE female_document_ids;
DROP TABLE word_count_docs;
