import json
import os

from src.sql.sql_manager import DBConnect


def update_atm_db(map_name):
    sql = DBConnect()

    atms = []
    for file in os.listdir(f"_files/atms/{map_name}"):
        with open(f"_files/atms/{map_name}/{file}", "r") as fin:
            atms.append(json.load(fin))

    for atm in atms:
        atm: dict
        plain_id = atm["m_PlainID"]
        username = atm["m_Username"]
        owned_currency = atm["m_OwnedCurrency"]
        mocb = atm["m_MaxOwnedCurrencyBonus"]

        sql.insert_into_player_atms(map_name, plain_id, username, owned_currency, mocb)
    sql.commit()
    sql.close()