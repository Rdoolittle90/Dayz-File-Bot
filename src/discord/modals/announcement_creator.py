import datetime
from discord import TextInputStyle
from nextcord.ui import Modal, TextInput
from nextcord import Interaction, Embed
from src.discord.guild_manager import get_server_settings
from src.discord.bot import DiscordBot


class AnnouncementCreator(Modal):
    """
    A modal for creating embedded announcements
    """
    def __init__(self, bot: DiscordBot, preview=0) -> None:
        """
        Initializes the EnterSteamID modal.
        """
        super().__init__(title="Announcement Form", timeout=(5 * 60))
        self.bot: DiscordBot = bot
        self.is_preview = preview
        
        self.color = TextInput(
            label="Color",
            placeholder="0xffffff",
            default_value="0xffffff",
            min_length=1,
            max_length=35,
            required=False
        )
        self.add_item(self.color)



    async def callback(self, interaction: Interaction) -> None:
        """
        """
        await interaction.response.defer(ephemeral=False)

        # Create a new Embed object with the input values
        # embed = Embed(
        #     title=self.title.value,
        #     description=self.description.value,
        #     color=self.color.value
        # )

        # if self.is_preview:
        #     channel = interaction.channel
        # else:
        #     settings = get_server_settings()
        #     channel = self.bot.get_channel(settings["announcement_channel"])

        # await channel.send(embed=embed)
        print("done.")