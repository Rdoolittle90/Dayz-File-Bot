from nextcord.ui import Modal, TextInput
from nextcord import Interaction
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
        
        self.title = TextInput(
            label="Title",
            placeholder="announcement title here",
            default_value="Platinum Server Announcement",
            min_length=1,
            max_length=100,
            required=False
        )
        self.add_item(self.title)
        
        self.title = TextInput(
            label="Summary description",
            placeholder="short and sweet",
            default_value="Details Below",
            min_length=1,
            max_length=35,
            required=False
        )
        self.add_item(self.title)



    async def callback(self, interaction: Interaction) -> None:
        """
        """
        await interaction.response.defer(ephemeral=False)

        await interaction.channel.send("🐈")