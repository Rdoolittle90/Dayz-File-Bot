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



    async def callback(self, interaction: Interaction) -> None:
        """
        """
        await interaction.response.defer(ephemeral=False)

        await interaction.channel.send("🐈")
        print("done.")