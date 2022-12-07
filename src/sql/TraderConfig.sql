USE s76891_PlatinumDayz;

# ----------------------------------------------------------------------------------------
SELECT * FROM traderconfig WHERE DUID = 919677581824000070 AND MapName = "Chernarus" AND ClassName LIKE "%pokemon%" LIMIT 0, 2500;


UPDATE typestable
SET _Usage = NULL
WHERE
	_Usage = ""
		AND
	MapName = "Namalsk";