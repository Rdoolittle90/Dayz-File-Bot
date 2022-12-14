import os

from disnake import ApplicationCommandInteraction
from disnake.ui import Select, View

from src.dayz.traderconfig_manager import TraderConfigManager


class load_traderconfig(Select):
    def __init__(self, options):
        super().__init__(placeholder="Select a map", max_values=1, min_values=1, options=options)
    
    async def callback(self, interaction: ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)
        if self.values[0] in os.listdir(f"_files/{interaction.guild.id}/maps"):
            message = await interaction.author.send(f"Loading TraderConfig from {interaction.guild.name} {self.values[0]}")
            tcm = TraderConfigManager()
            await tcm.load_traderconfig_to_db(message, interaction.guild.id, self.values[0])
            await interaction.followup.send("Done!")
        else:
            await interaction.followup.send("Coming Soon!")


class load_traderconfig_view(View):
    def __init__(self, options, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(load_traderconfig(options))

