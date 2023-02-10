import json
import os
from disnake import ModalInteraction
from disnake.ui import Modal, TextInput
from src.dayz.atm_manager import get_player_info_from_any_atm_file
from src.ftp.ftp_manager import FTPConnect

from src.sql.sql_manager import DBConnect


class Registration(Modal):
    def __init__(self) -> None:
        components: list = [
            TextInput(
                label="Steam64",
                placeholder="12345678910111213",
                custom_id=f"steam_id",
                min_length=17,
                max_length=17,
                required=True
            )
        ]
        super().__init__(title="Enter Your Steam64 ID", components=components)
    

    async def callback(self, interaction:ModalInteraction) -> None:
        await interaction.response.defer(ephemeral=True)
        user_input: str = interaction.data["components"][0]["components"][0]["value"]
        try:
            sql = DBConnect()

            sql.check_if_SK64_in_registration(int(user_input))
            SK64_found = sql.c.fetchone()[0]

            sql.check_if_DUID_in_registration(interaction.author.id)
            DUID_found = sql.c.fetchone()[0]

            print(SK64_found, DUID_found)
            if SK64_found and not DUID_found:
                print(f"{user_input} Available")
                sql.update_registration(int(user_input), interaction.author.id)
                sql.commit()

                player_file = get_player_info_from_any_atm_file(int(user_input))[0]
                print(player_file)


                await interaction.author.edit(nick=player_file[0]['playername'])
                await interaction.author.add_roles(1072971824620650556, reason="Registered via Drifter")
                await interaction.followup.send(f"Done! Welcome to Platinum Servers {player_file[0]['playername']}")

            elif SK64_found and DUID_found:
                print(f"{SK64_found} Already Taken {DUID_found}")
                await interaction.followup.send(f"This Account is already taken.")

            else:
                print(f"{user_input} Not Found")
                get_atms()
                await interaction.followup.send(f"This Account was not found try again in a few minutes.")

            sql.close()

        except ValueError as err:
            print(err)
            await interaction.followup.send("Something doesnt look right")


def get_atms():
    sql = DBConnect()
    sql_cmmd = "INSERT IGNORE INTO registration (SK64) VALUES (%s)"

    for folder_name in os.listdir("_files\919677581824000070\maps"):
        print(folder_name)
        ftp = FTPConnect(folder_name) #FIXME
        ftp.connect()
        ftp.getAllPlayerATM(919677581824000070)
        for file_name in os.listdir(f"_files\919677581824000070\maps\{folder_name}\\atms"):
            sql.c.execute(sql_cmmd, (file_name.strip(".json"), ))
        sql.commit()
        ftp.ftp.close()
    sql.close()
