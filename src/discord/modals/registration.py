from disnake import ModalInteraction
from disnake.ui import Modal, TextInput

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
        user_input: str = interaction.data["components"][0]["components"][0]["value"]
        try:
            sql = DBConnect()
            sql.select_DUID_from_registration(int(user_input))
            DUID = sql.c.fetchone()
            print(DUID)

        except ValueError as err:
            print(err)

