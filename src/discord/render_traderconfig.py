from disnake import Activity, ActivityType, ApplicationCommandInteraction, Embed, SelectOption, Status
from disnake.ui import View, Select
from disnake import File as disnake_File
from src.dayz.traderconfig_manager import TraderConfigManager

from src.dayz.xml_manager import XMLManager



class render_traderconfig(Select):
    def __init__(self):
        options=[
            SelectOption(label="Namalsk", emoji="❄️"),
            SelectOption(label="Chernarus", emoji="🌲")
            ]
        super().__init__(placeholder="Select a map",max_values=1,min_values=1,options=options)
    
    async def callback(self, interaction: ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)
        bot = interaction.bot
        author = interaction.author

        activity = Activity(type=ActivityType.custom, name=F"{self.values[0]} TraderFile.txt")
        await bot.change_presence(status=Status.dnd, activity=activity)
        message = await interaction.author.send("This will take some time please dont run any commands until this has either completed or failed\nAVG: completion time is 5min")
        
        if self.values[0] in ["Namalsk", "Chernarus"]:
            
            tcm = TraderConfigManager()
            await tcm.create_new_traderconfig(message, "Namalsk")
            await interaction.author.send(file=disnake_File(f'_files/outputs/{self.values[0]}/TraderConfig.txt'))
            await interaction.followup.send("TraderConfig.txt Complete!")



class render_traderconfig_view(View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(render_traderconfig())

