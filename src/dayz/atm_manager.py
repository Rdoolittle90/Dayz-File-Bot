import json
import os
from disnake import ApplicationCommandInteraction, Embed
from src.ftp.ftp_manager import FTPConnect
from src.sql.sql_manager import DBConnect


maps = ["Chernarus", "Takistan", "Namalsk", "TestServer"]


def update_atms(SK64):
    for map_name in maps:
        ftp = FTPConnect(map_name)
        ftp.connect()
        ftp.getOnePlayerATM(SK64)
        ftp.ftp.close()


async def display_player_atm(interaction:ApplicationCommandInteraction, DUID):
    sql = DBConnect()
    sql.check_if_DUID_in_registration(DUID)
    result = sql.c.fetchone()

    sql.select_SK64_from_registration(DUID)
    SK64 = sql.c.fetchone()
    print(SK64[0])

    if result:
        update_atms(SK64[0])
        player_atms = get_player_info_from_any_atm_file(SK64[0])
        player_name = player_atms[0][1]["playername"]
        if player_name.endswith("s"):
            player_name += "'"
        else:
            player_name += "'s"


        embed = Embed(title=f"{player_name} ATM", description="Showing ATMs for all maps found.")
        for atm in player_atms:
            embed.add_field(name=atm[0], value=f"{atm[1]['currentMoney']:,} ₽", inline=True)
        message = await interaction.followup.send(embed=embed, ephemeral=True)
        return (embed, message)
    else:
        await interaction.followup.send("You Dont seem to have an account.")


def update_player_atm(map_name:str, DUID:int, amount:int, SK64=None):
    ftp = FTPConnect(map_name) #FIXME
    ftp.connect()

    sql = DBConnect()
    if SK64 is None:
        sql.select_SK64_from_registration(DUID)
        SK64 = sql.c.fetchone()
        if SK64:
            SK64 = int(SK64[0])
    else:
        sql.check_if_SK64_in_registration(SK64)
        result = sql.c.fetchone()
        if not result:
            return 0
    sql.close()
    ftp.getOnePlayerATM(SK64)
    ftp.UpdateATM(SK64, map_name, amount)

    ftp.quit()
    return 1

    # SK64 not found
    print("ID not found")
    ftp.quit()
    return 0


def get_player_info_from_any_atm_file(SK64):
    found_atms = []
    for folder_name in os.listdir("_files/919677581824000070/maps"):
        if f"{SK64}.json" in os.listdir(f"_files/919677581824000070/maps/{folder_name}/atms"):
            with open(f"_files/919677581824000070/maps/{folder_name}/atms/{SK64}.json", "r") as fin:
                player_file = json.load(fin)
            found_atms.append((folder_name, player_file))
    return found_atms


def open_player_atm(SK64, map_name):
    if f"{SK64}.json" in os.listdir(f"_files/919677581824000070/maps/{map_name}/atms"):
        with open(f"_files/919677581824000070/maps/{map_name}/atms/{SK64}.json", "r") as fin:
            player_file = json.load(fin)
            return player_file