USE s76891_MuninnPlatinum;

# ----------------------------------------------------------------------------------------
SELECT * FROM itemvalues;

# ----------------------------------------------------------------------------------------
LOAD DATA LOCAL
    INFILE 'file_name'
    REPLACE
    INTO TABLE typestable;

# ----------------------------------------------------------------------------------------
SELECT
	* 
FROM 
	itemtags
WHERE 
	MapName = "Namalsk"
		AND
	ClassTag = "floor";

# ----------------------------------------------------------------------------------------
SELECT 
	* 
FROM 
	itemvalues 
WHERE 
	MapName = "Namalsk" 
		AND 
	ClassName LIKE "landmine%";

# ----------------------------------------------------------------------------------------
SELECT
	* 
FROM 
	item_usage;

# ----------------------------------------------------------------------------------------
SELECT
	*
FROM
	traderconfig 
WHERE 
	MapName = "Namalsk" 
AND 
	ClassName 
LIKE
	"%bl_sofa_%";

# ----------------------------------------------------------------------------------------
SELECT
	*
FROM
	traderconfig
WHERE 
	MapName = "Namalsk"
		AND 
	ClassName LIKE "%canna%";

# ----------------------------------------------------------------------------------------
SELECT 
	Category, 
    Max(BuyValue), 
    Max(SellValue) 
FROM 
	traderconfig
WHERE 
	MapName = "Namalsk" 
		AND 
	Trader = "BlackMarketTrader" 
GROUP BY Category;

# ----------------------------------------------------------------------------------------
CALL select_trader_category_products("Namalsk", "HelicopterTrader", "Helicopters");

# ----------------------------------------------------------------------------------------
DROP PROCEDURE select_traderconfig_stats;

# ----------------------------------------------------------------------------------------
UPDATE typestable
SET
	CntInCargo = 0,
	CntInMap = 1
WHERE 
	MapName = "Namalsk"
		AND 
	ClassName LIKE "%collectable_%"
		AND
	CntInCargo = 1;


# ----------------------------------------------------------------------------------------
SELECT
	* 
FROM 
	traderconfig 
WHERE
	MapName = "Namalsk" 
		AND 
	Trader = "ClothingTrader";

# ----------------------------------------------------------------------------------------
SELECT 
	* 
FROM 
	traderconfig 
WHERE 
	Trader = "HelicopterTrader"
		AND 
	Category = "Helicopters" 
ORDER BY 
	SellValue DESC;

# ----------------------------------------------------------------------------------------
SELECT 
	* 
FROM
	typestable
WHERE
	MapName = "Namalsk"
		AND
	ClassName LIKE "%doll%"
		AND
	(
	Trader = "BlackMarketTrader"
		OR
	Trader = "TheCollector"
    );
C:\Users\COFsl\OneDrive\Documents\scripts\platinumserver\sheet2.sql
# ----------------------------------------------------------------------------------------
UPDATE 
	traderconfig 
SET 
	Category = "Suppressors, Compensators, and Barrels"
WHERE
	MapName = "Namalsk"
		AND
	Category = "Suppressors,Compensators,andBarrels";

# ----------------------------------------------------------------------------------------BlackMarketTrader ClothingTrader Suppressors, Compensators, and Barrels
UPDATE 
	typestable 
SET 
	Restock = 20000
WHERE
	ClassName LIKE "Collectable_pokemon%";

# ----------------------------------------------------------------------------------------
SELECT * FROM traderconfig WHERE Trader LIKE "B%";

# ----------------------------------------------------------------------------------------
# DELETE FROM typestable WHERE ClassName LIKE "Collectable_pokemon%";

# ----------------------------------------------------------------------------------------
ALTER TABLE itemtags DROP FOREIGN KEY itemtags_ibfk_1;

# ----------------------------------------------------------------------------------------
ALTER TABLE itemvalues DROP FOREIGN KEY itemvalues_ibfk_1;

# ----------------------------------------------------------------------------------------
ALTER TABLE itemvalues
ADD FOREIGN KEY (ClassName) REFERENCES typestable(ClassName)
	ON DELETE CASCADE;

# ----------------------------------------------------------------------------------------
ALTER TABLE itemusage
ADD FOREIGN KEY (ClassName) REFERENCES typestable(ClassName)
	ON DELETE CASCADE;

# ----------------------------------------------------------------------------------------
SELECT 
	TC.ClassName,
    TT.*,
    TC.Trader,
    TC.Category,
    TC.VendorFlag,
    TC.BuyValue,
    TC.SellValue
FROM
	typestable TT
LEFT JOIN 
	traderconfig TC 
		on 
			TC.ClassName = TT.ClassName
WHERE 
	TT.ClassName 
		LIKE 
			"Collectable_poke%"
ORDER BY 
	TT.Nominal ASC;

# ----------------------------------------------------------------------------------------
DELIMITER //
CREATE PROCEDURE select_like_product(IN product_name VARCHAR(60))
	BEGIN
		SELECT TC.ClassName, TT.*, TC.Trader, TC.Category, TC.VendorFlag, TC.BuyValue, TC.SellValue
		FROM typestable TT
		LEFT JOIN traderconfig TC on TC.ClassName = TT.ClassName
		WHERE TT.ClassName LIKE CONCAT("%",product_name,"%")
		ORDER BY TC.SellValue ASC;
    END //
DELIMITER ;

# ----------------------------------------------------------------------------------------
CALL select_like_product("pokemon");

# ----------------------------------------------------------------------------------------
CALL select_typestable_stats(0, 0);


# ----------------------------------------------------------------------------------------
DELIMITER //
CREATE PROCEDURE select_trader_category_products(IN _trader VARCHAR(60), IN _category VARCHAR(60))
BEGIN
	SELECT ClassName, VendorFlag, BuyValue, SellValue
	FROM traderconfig
	WHERE Trader = _trader AND Category = _category
	ORDER BY SellValue DESC, ClassName ASC;
END //
DELIMITER ;

# ----------------------------------------------------------------------------------------
CALL select_map_traders_fix("Namalsk");

# ----------------------------------------------------------------------------------------
CALL select_map_trader_categories("Namalsk", "TheCollector");

# ----------------------------------------------------------------------------------------
CALL select_map_trader_category_products("Namalsk", "TheCollector", "GameBoyGames");











SELECT
	*
FROM
	traderconfig
WHERE
	MapName = "Namalsk"
ORDER BY
	CASE 
		WHEN SellValue = -1 THEN BuyValue
		ELSE SellValue
	END DESC;


