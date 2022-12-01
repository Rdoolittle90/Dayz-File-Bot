# ----------------------------------------------------------------------------------------
SELECT * FROM typestable WHERE ClassName LIKE "cab%";

SELECT DISTINCT(_Tags) FROM typestable WHERE _Tags IS NOT NULL ORDER BY _Tags ASC;