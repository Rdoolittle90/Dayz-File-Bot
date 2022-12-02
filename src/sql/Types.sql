# ----------------------------------------------------------------------------------------
SELECT * FROM typestable WHERE ClassName LIKE "%pokemonc%";


SELECT ClassName FROM typestable WHERE _Tags = "hunting,military";
SELECT _Tags, COUNT(_Tags) FROM typestable WHERE MapName = "Nemalsk" AND _Tags IS NOT NULL GROUP BY _Tags;
SELECT _Tier, COUNT(_Tier) FROM typestable WHERE MapName = "Nemalsk" AND _Tier IS NOT NULL GROUP BY _Tier;

UPDATE typestable
SET _Tags = NULL
WHERE _Tags = "floor";
