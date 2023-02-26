from nextcord import Color, Embed, Interaction, ui
# Modal, TextInput, View

from src.file_manager import get_map_key, remove_embed, remove_map_dir



class RemoveMapModal(ui.Modal):
    def __init__(self) -> None:
        super().__init__(title="Select an Option Catagory")
        self.map_name = ui.TextInput(
            label="Map Name",
            placeholder="Namalsk",
            custom_id=f"map",
            min_length=1,
            max_length=25,
            required=True
        )
        self.add_item(self.map_name)

        self.map_key = ui.TextInput(
            label="Enter passkey",
            placeholder="use /get_key",
            custom_id=f"passkey",
            min_length=16,
            max_length=16,
            required=True
        )
        self.add_item(self.map_key)
        

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.defer(ephemeral=False)
        map_key: str = get_map_key(self.map_name.value)["passkey"]
        
        if self.map_key.value == map_key:
            remove_map_dir(self.map_name.value)
            await interaction.followup.send(embed=remove_embed(self.map_name.value))
        else:
            failed_deletion = Embed(
                title="Map Deletion Failed!", 
                description="Either the map name or passkey is wrong", 
                color=Color.red()
            )
            await interaction.followup.send(embed=failed_deletion)
