import os
from disnake import ApplicationCommandInteraction, Color, Embed, SelectOption
from disnake.ui import View, Select
from disnake import File as disnake_File
from disnake import Status, Game, Activity, ActivityType

from src.dayz.xml_manager import XMLManager



class render_types(Select):
    def __init__(self):
        """"""
        options=[
            SelectOption(label="Namalsk", emoji="❄️"),
            SelectOption(label="Chernarus", emoji="🌲"),
            SelectOption(label="Takistan", emoji="🌵")
            ]
        super().__init__(placeholder="Select a map",max_values=1,min_values=1,options=options)
    
    async def callback(self, interaction: ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)
        bot = interaction.bot
        author = interaction.author

        activity = Activity(type=ActivityType.custom, name=F"{self.values[0]} types.xml")
        await bot.change_presence(status=Status.dnd, activity=activity)

        message = await interaction.author.send("This will take some time please dont run any commands until this has either completed or failed\nAVG: completion time is 37min")

        if self.values[0] in os.listdir("_files/maps"):
            xmlm = XMLManager()
            await xmlm.create_new_types(message, self.values[0])

            await author.send(file=disnake_File(f'_files/maps/{self.values[0]}/outputs/types.xml'))
            await bot.change_presence(status=Status.online, activity=None)
            await interaction.followup.send("Done.")

class render_types_view(View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(render_types())

