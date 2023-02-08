import os
from disnake import ModalInteraction
from disnake.ui import Modal, TextInput
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
        await interaction.response.defer(ephemeral=False)
        
        sql = DBConnect()
        sql_cmmd = "INSERT IGNORE INTO registration (SK64) VALUES (%s)"

        for folder_name in os.listdir("_files\919677581824000070\maps"):
            print(folder_name)
            ftp = FTPConnect(folder_name) #FIXME
            ftp.getAllPlayerATM(919677581824000070)
            ftp.connect()
            for file_name in os.listdir(f"_files\919677581824000070\maps\{folder_name}\\atms"):
                sql.c.execute(sql_cmmd, (file_name.strip(".json"), ))
            sql.commit()
            ftp.ftp.close()
        sql.close()

        user_input: str = interaction.data["components"][0]["components"][0]["value"]
        try:
            sql = DBConnect()
            sql.check_if_SK64_in_registration(int(user_input))
            SK64 = sql.c.fetchone()
            sql.close()
            print(SK64)

        except ValueError as err:
            print(err)

