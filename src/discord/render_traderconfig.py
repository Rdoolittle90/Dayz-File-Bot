import os

from disnake import Activity, ActivityType, ApplicationCommandInteraction, Embed, SelectOption, Status
from disnake import File as disnake_File

from disnake.ui import View, Select

from src.dayz.traderconfig_manager import TraderConfigManager



class render_traderconfig(Select):
    def __init__(self, options):
        super().__init__(placeholder="Select a map", max_values=1, min_values=1, options=options)
    
    async def callback(self, interaction: ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)
        bot = interaction.bot
        author = interaction.author

        activity = Activity(type=ActivityType.custom, name=F"{self.values[0]} TraderFile.txt")
        await bot.change_presence(status=Status.dnd, activity=activity)
        message = await interaction.author.send("This will take some time please dont run any commands until this has either completed or failed\nAVG: completion time is 5min")
        

        if self.values[0] in os.listdir("_files/{self.guid}/maps"):
            tcm = TraderConfigManager()
            await tcm.create_new_traderconfig(message, self.values[0])
            await interaction.author.send(file=disnake_File(f'_files/{self.guid}/maps/{self.values[0]}/outputs/TraderConfig.txt'))
            await bot.change_presence(status=Status.online, activity=None)
            await interaction.followup.send("TraderConfig.txt Complete!")
        else:
            await interaction.followup.send("Coming Soon!")



class render_traderconfig_view(View):
    def __init__(self, options, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(render_traderconfig(options))

