import datetime
from discord import TextInputStyle
from nextcord.ui import Modal, TextInput
from nextcord import Interaction, Embed
from src.discord.guild_manager import get_server_settings
from src.discord.bot import DiscordBot


class AnnouncementCreator(Modal):
    """
    A modal for entering a Steam 64 ID.
    """
    def __init__(self, bot: DiscordBot, preview=0) -> None:
        """
        Initializes the EnterSteamID modal.
        """
        super().__init__(title="Registration Form", timeout=(5 * 60))
        self.bot: DiscordBot = bot
        self.is_preview = preview

        color_id = bot.generate_random_string(8)
        title_id = bot.generate_random_string(8)
        descr_id = bot.generate_random_string(8)

        
        self.color = TextInput(
            label="Color",
            placeholder="enter color",
            custom_id=f"title_{color_id}",
            min_length=1,
            max_length=35,
            required=False
        )
        self.add_item(self.color)

        self.title = TextInput(
            label="Title",
            placeholder="enter title",
            custom_id=f"title_{title_id}",
            min_length=1,
            max_length=35,
            required=True
        )
        self.add_item(self.title)

        self.description = TextInput(
            style=TextInputStyle.paragraph,
            label="Description",
            placeholder="enter description",
            custom_id=f"description_{descr_id}",
            min_length=1,
            max_length=1000,
            required=True
        )
        self.add_item(self.description)



    async def callback(self, interaction: Interaction) -> None:
        """
        """
        await interaction.response.defer(ephemeral=False)


        if not self.color.value:
            self.color.value = 0xffffff

        # Create a new Embed object with the input values
        embed = Embed(
            title=self.title.value,
            description=self.description.value,
            color=self.color.value
        )

        if self.is_preview:
            channel = interaction.channel
        else:
            settings = get_server_settings()
            channel = self.bot.get_channel(settings["announcement_channel"])

        await channel.send(embed=embed)