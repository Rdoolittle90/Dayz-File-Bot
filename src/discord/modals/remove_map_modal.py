from disnake import ModalInteraction
from disnake.ui import Modal, Select, TextInput

from src.discord.guild_manager import get_map_selections


class RemoveMapModal(Modal):
    def __init__(self, interaction) -> None:
        components: list = [
            Select(
                custom_id="map",
                placeholder="Select a Map",
                options=get_map_selections(interaction.guild.id)
            ),
            TextInput(
                label="Enter passkey",
                placeholder="",
                custom_id=f"passkey",
                min_length=16,
                max_length=16,
                required=True
            )
        ]
        super().__init__(title="Select an Option Catagory", components=components)
    

    async def callback(self, interaction: ModalInteraction) -> None:
        map: str = interaction.data["components"][0]["components"][0]["values"][0]
        passkey: str = interaction.data["components"][0]["components"][0]["value"]

        print(map)
        print(passkey)