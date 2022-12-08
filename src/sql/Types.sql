# ----------------------------------------------------------------------------------------
SELECT * FROM typestable WHERE ClassName LIKE "%pokemonc%" AND MapName = "Takistan" AND DUID = 919677581824000070;
DELETE FROM typestable WHERE ClassName NOT LIKE "%pokemonc%" AND MapName = "Takistan" AND DUID = 919677581824000070;


SELECT ClassName FROM typestable WHERE _Tags = "industrial";
SELECT _Tags, COUNT(_Tags) FROM typestable WHERE MapName = "Takistan" AND _Tags IS NOT NULL GROUP BY _Tags;
SELECT _Tags, COUNT(_Tags) FROM typestable WHERE MapName = "Namalsk" AND _Tags IS NOT NULL GROUP BY _Tags;

UPDATE typestable
SET _Tags = NULL
WHERE _Tags = "floor";
