USE s76891_PlatinumDayz;

DROP TABLE traderconfig;
CREATE TABLE traderconfig (
	MapName VARCHAR(35) NOT NULL,
	Trader VARCHAR(35) NOT NULL,
	Category VARCHAR(60) NOT NULL,
	ClassName VARCHAR(60) NOT NULL,
	VendorFlag VARCHAR(10) NOT NULL,
	BuyValue INT NOT NULL,
	SellValue INT NOT NULL,
	PRIMARY KEY (MapName, Trader, ClassName)
);

DROP TABLE typestable;
CREATE TABLE typestable(
	MapName VARCHAR(35) NOT NULL,
	ClassName VARCHAR(60) NOT NULL,
	Category VARCHAR(60) NOT NULL,
	Nominal TINYINT,
	Lifetime MEDIUMINT NOT NULL,
	Restock MEDIUMINT,
	_Min TINYINT,
	Quantmin SMALLINT,
	Quantmax SMALLINT,
	Cost TINYINT,
	_Tier VARCHAR(20),
	_Usage VARCHAR(60),
	_Tags VARCHAR(60),
	CntInMap BOOLEAN NOT NULL,
	CntInHoarder BOOLEAN NOT NULL,
	CntInCargo BOOLEAN NOT NULL,
	CntInPlayer BOOLEAN NOT NULL,
	Crafted BOOLEAN NOT NULL,
	Deloot BOOLEAN NOT NULL,
	PRIMARY KEY (MapName, ClassName)
);
CREATE INDEX typestable_category_idx ON typestable(Category);
CREATE INDEX typestable_mapname_idx ON typestable(MapName);


CREATE TABLE player_atms(
	MapName VARCHAR(35) NOT NULL,
    PlainID BIGINT UNSIGNED NOT NULL,
    UserName VARCHAR(60) NOT NULL,
    OwnedCurrency MEDIUMINT UNSIGNED NOT NULL,
    MaxOwnedCurrencyBonus SMALLINT UNSIGNED NOT NULL,
    DID BIGINT UNSIGNED,
    PRIMARY KEY (MapName, PlainID)
);

CREATE TABLE server_mods(
	MapName VARCHAR(35),
    _Directory VARCHAR(35),
    Disabled BOOLEAN,
    FileID BIGINT UNSIGNED,
    ServerSide BOOLEAN,
    PRIMARY KEY (MapName, FileID)
);



delimiter //
CREATE PROCEDURE select_map_traders (IN _mapname VARCHAR(35))
	BEGIN
		SELECT Trader
		FROM traderconfig
        GROUP BY Trader;
	END//
delimiter ;

delimiter //
CREATE PROCEDURE select_map_trader_categories (IN _mapname VARCHAR(35), IN _trader VARCHAR(60))
	BEGIN
		SELECT Category
		FROM traderconfig
		WHERE Trader = _trader
        GROUP BY Category;
	END//
delimiter ;

delimiter //
CREATE PROCEDURE select_map_trader_category_products (IN _mapname VARCHAR(35), IN _trader VARCHAR(30), IN _category VARCHAR(60))
	BEGIN
		SELECT ClassName, VendorFlag, BuyValue, SellValue
		FROM traderconfig
        WHERE 
			MapName = _mapname
				AND
			Trader = _trader
				AND
			Category = _category;
	END//
delimiter ;

delimiter //
CREATE PROCEDURE select_stats (IN _mapname VARCHAR(30), OUT trader_count SMALLINT, OUT item_count MEDIUMINT)
	BEGIN
		SELECT COUNT( DISTINCT Trader)
		FROM traderconfig
        WHERE MapName = _mapname
        INTO trader_count;
        
		SELECT COUNT( DISTINCT ClassName)
        FROM traderconfig
        WHERE MapName = _mapname
        INTO item_count;
	END//
delimiter ;

CALL select_traders();
CALL select_categorys("BlackMarketTrader");
CALL select_products("BlackMarketTrader", "LuxuryItems");

CALL select_stats("Namalsk", @val1, @val2);
SELECT @val1;
SELECT @val2;
