from disnake import Color, Embed, ModalInteraction
from disnake.ui import Modal, TextInput

from src.file_manager import get_map_key, remove_embed, remove_map_dir



class RemoveMapModal(Modal):
    def __init__(self) -> None:
        components: list = [
            TextInput(
                label="Map Name",
                placeholder="Namalsk",
                custom_id=f"map",
                min_length=1,
                max_length=25,
                required=True
            ),
            TextInput(
                label="Enter passkey",
                placeholder="use /get_key",
                custom_id=f"passkey",
                min_length=16,
                max_length=16,
                required=True
            )
        ]
        super().__init__(title="Select an Option Catagory", components=components)
    

    async def callback(self, interaction:ModalInteraction) -> None:
        await interaction.response.defer(ephemeral=False)
        print(interaction.data["components"])
        map_str: str = interaction.data["components"][0]["components"][0]["value"]
        passkey: str = interaction.data["components"][1]["components"][0]["value"]
        map_key: str = get_map_key(interaction.guild.id, map_str)
        print(map_str)
        print(passkey)
        print(map_key)
        
        if passkey == map_key:
            remove_map_dir(interaction.guild.id, map_str)
            await interaction.followup.send(embed=remove_embed(map_str))
        else:
            failed_deletion = Embed(
                title="Map Deletion Failed!", 
                description="Either the map name or passkey is wrong", 
                color=Color.red()
            )
            await interaction.followup.send(embed=failed_deletion)