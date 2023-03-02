import datetime
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

        self.title = TextInput(
            label="Title",
            placeholder="enter title",
            custom_id=f"title_{bot.generate_random_string(8)}",
            min_length=1,
            max_length=35,
            required=True
        )
        self.add_item(self.title)

        self.description = TextInput(
            label="Description",
            placeholder="enter description",
            custom_id=f"description_{bot.generate_random_string(8)}",
            min_length=1,
            max_length=35,
            required=True
        )
        self.add_item(self.description)



    async def callback(self, interaction: Interaction) -> None:
        """
        """
        await interaction.response.defer(ephemeral=False)

        # Create a new Embed object with the input values
        embed = Embed(
            title=self.title.value,
            description=self.description.value,
            timestamp=datetime.datetime.utcnow()
        )

        if self.is_preview:
            channel = interaction.channel
        else:
            settings = get_server_settings()
            channel = self.bot.get_channel(settings["announcement_channel"])

        await channel.send(embed=embed)