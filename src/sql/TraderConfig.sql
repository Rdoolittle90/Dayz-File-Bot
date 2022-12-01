USE s76891_PlatinumDayz;

# ----------------------------------------------------------------------------------------
SELECT * FROM typestable WHERE MapName = "Namalsk" AND Restock = 1800;


UPDATE typestable
SET _Usage = NULL
WHERE
	_Usage = ""
		AND
	MapName = "Namalsk";