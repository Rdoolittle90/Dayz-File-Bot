USE s76891_PlatinumDayz;

# ----------------------------------------------------------------------------------------
SELECT * FROM traderconfig WHERE DUID = 1004866053043667007 LIMIT 0, 10000;
DELETE FROM traderconfig WHERE DUID = 1004866053043667007;

UPDATE typestable
SET _Usage = NULL
WHERE
	_Usage = ""
		AND
	MapName = "Namalsk";
    
SET @_duid = 919677581824000070;
START TRANSACTION;
	UPDATE traderconfig SET Trader = "Black Market Trader" WHERE DUID = @_duid AND Trader = "BlackMarketTrader";
	UPDATE traderconfig SET Trader = "Clothing Trader" WHERE DUID = @_duid AND Trader = "ClothingTrader";
	UPDATE traderconfig SET Trader = "Consume Trader" WHERE DUID = @_duid AND Trader = "ConsumeTrader";
	UPDATE traderconfig SET Trader = "Fishing Supplies" WHERE DUID = @_duid AND Trader = "FishingSupplies";
	UPDATE traderconfig SET Trader = "Hardware Supplies" WHERE DUID = @_duid AND Trader = "MiscTrader";
	UPDATE traderconfig SET Trader = "Hunting Supplies" WHERE DUID = @_duid AND Trader = "HuntingSupplies";
	UPDATE traderconfig SET Trader = "The Collector" WHERE DUID = @_duid AND Trader = "TheCollector";
	UPDATE traderconfig SET Trader = "Vehicles Trader" WHERE DUID = @_duid AND Trader = "VehiclesTrader";
	UPDATE traderconfig SET Trader = "Weapon Supplies" WHERE DUID = @_duid AND Trader = "WeaponSupplies";
	UPDATE traderconfig SET Trader = "Weapon Trader" WHERE DUID = @_duid AND Trader = "WeaponTrader";
COMMIT;