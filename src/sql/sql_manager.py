import mysql.connector
import datetime

from os import getenv
from dotenv import load_dotenv

load_dotenv()


class DBConnect():
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = getenv("SQL_HOST"),
            user = getenv("SQL_USER"),
            passwd = getenv("SQL_PASSWORD"),
            database = getenv("SQL_DB")
            )
        self.c = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.c.close()
        self.conn.close()

    def insert_into_typestable(self, list_object):
        sql = """
            INSERT IGNORE INTO
                typestable
                    (DUID, MapName, ClassName, Category, Nominal, Lifetime,
                    Restock, _Min, Quantmin, Quantmax, Cost, _Tier, _Usage, _Tags,
                    CntInMap, CntInHoarder, CntInCargo, CntInPlayer, Crafted, Deloot)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY
                UPDATE
                    Category = %s,
                    Nominal = %s,
                    _Min = %s,
                    Cost = %s
"""
        self.c.execute(sql, list_object)
        
    
    def insert_into_traderconfig(self, DUID, map_name, trader, category, classname, vendorflag, buyvalue, sellvalue):
        sql = """
            INSERT INTO
                traderconfig
                    (DUID, MapName, Trader, Category, ClassName, VendorFlag, BuyValue, SellValue)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY
                UPDATE
                    VendorFlag = %s,
                    BuyValue = %s,
                    SellValue = %s
"""
        self.c.execute(sql, (DUID, map_name, trader, category, classname, vendorflag, buyvalue, sellvalue, 
            vendorflag, buyvalue, sellvalue))


    def insert_into_player_atms(self, DUID, map_name, PlainID, UserName, OwnedCurrency, MaxOwnedCurrencyBonus):
        sql = """
            INSERT INTO
                player_atms
                    (DUID, MapName, PlainID, UserName, OwnedCurrency, MaxOwnedCurrencyBonus)
                VALUES
                    (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY
                UPDATE
                    OwnedCurrency = %s,
                    MaxOwnedCurrencyBonus = %s
"""
        self.c.execute(sql, (DUID, map_name, PlainID, UserName, OwnedCurrency, MaxOwnedCurrencyBonus, OwnedCurrency, MaxOwnedCurrencyBonus))


    
    def insert_into_server_mods(self, DUID, map_name, mod_dict):
        sql = """
            INSERT INTO
                server_mods
                    (DUID, MapName, _Directory, Disabled, FileID, ServerSide)
                VALUES
                    (%s, %s, %s, %s, %s, %s)     
            ON DUPLICATE KEY
                UPDATE
                    Disabled = %s
"""
        self.c.execute(sql, (DUID, map_name, mod_dict["directory"], mod_dict["disabled"], 
            mod_dict["file_id"], mod_dict["server_side"], mod_dict["disabled"]))

    def check_if_DUID_in_registration(self, DUID):
        sql = """ 
            SELECT
                CASE WHEN EXISTS
                (
                    SELECT * FROM registration WHERE DUID = %s
                )
                THEN True
                ELSE False
            END
"""
        self.c.execute(sql, (DUID, ))


    def check_if_SK64_in_registration(self, SK64):
        sql = """ 
            SELECT
                CASE WHEN EXISTS
                (
                    SELECT * FROM registration WHERE SK64 = %s
                )
                THEN True
                ELSE False
            END
"""
        self.c.execute(sql, (SK64, ))


    def update_registration(self, SK64, DUID):
        sql = """
            UPDATE 
                registration 
            SET 
                DUID = %s,
                regDate = %s
            WHERE 
                SK64 = %s
"""
        self.c.execute(sql, (DUID, datetime.datetime.now(), SK64))



    def select_SK64_from_registration(self, DUID):
        sql = """
            SELECT 
                SK64 
            FROM 
                registration 
            WHERE 
                DUID = %s
"""
        self.c.execute(sql, (DUID, ))


    def select_DUID_from_registration(self, SK64):
        sql = """
            SELECT 
                DUID 
            FROM 
                registration 
            WHERE 
                SK64 = %s
"""
        self.c.execute(sql, (SK64, ))

    def select_all_from_typestable(self, DUID, map_name):
        sql = """
        SELECT
            *
        FROM
            typestable
        WHERE
            DUID = %s
                AND
            MapName = %s
        ORDER BY
            ClassName
"""
        self.c.execute(sql, (DUID, map_name))
