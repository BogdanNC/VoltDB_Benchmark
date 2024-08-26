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
WHERE gender = 'male'
GROUP BY f.id_document;

INSERT INTO avg_doclen_and_total_ids (avrage, total_ids)
SELECT AVG(docLen) AS avrage, COUNT(ID) AS total_ids FROM doc_lengths;

INSERT INTO no_word_docs (id_word, noDocWords)
SELECT f.id_word AS id_word, COUNT (DISTINCT f.id_document) AS noDocWords
FROM document_facts f
INNER JOIN author_dimension ad on ad.id_author = f.id_author
WHERE gender = 'male'
GROUP BY f.id_word;

SELECT q2.id_document, SUM (q2.tfidf) AS stfidf
FROM (
    SELECT f.id_document, ( (1 + LOG(al.total_ids / ndw.noDocWords )) * f.tf ) AS tfidf
    FROM document_facts f
    INNER JOIN word_dimension wd ON wd.id_word = f.id_word
    INNER JOIN author_dimension ad ON ad.id_author = f.id_author
    INNER JOIN no_word_docs ndw ON ndw.id_word = f.id_word
    CROSS JOIN avg_doclen_and_total_ids al 
    WHERE
        ad.gender = 'male'
        and wd.word IN ('think', 'today', 'friday')
) q2 
GROUP BY q2.id_document
ORDER BY stfidf DESC, 1
LIMIT 10;

DROP TABLE doc_lengths;
DROP TABLE avg_doclen_and_total_ids;
DROP TABLE no_word_docs;
