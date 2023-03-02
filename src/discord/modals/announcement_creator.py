import datetime
from nextcord.ui import Modal, TextInput
from nextcord import Interaction, Embed
from src.discord.guild_manager import get_server_settings
from src.discord.bot import DiscordBot


class AnnouncementCreator(Modal):
    """
    A modal for entering a Steam 64 ID.
    """
    def __init__(self, bot: DiscordBot, num_fields=0, preview=0) -> None:
        """
        Initializes the EnterSteamID modal.
        """
        super().__init__(title="Registration Form", timeout=(5 * 60))
        self.bot: DiscordBot = bot
        self.preview = preview

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

        self.field_names = []
        self.field_values = []

        for field_num in range(num_fields):
            field_name = TextInput(
                label=f"Field {field_num} Title",
                placeholder=f"field {field_num} title",
                custom_id=f"field_name_{field_num}_{bot.generate_random_string(8)}",
                min_length=1,
                max_length=35,
                required=True
            )
            self.field_names.append(field_name)
            self.add_item(field_name)

            field_value = TextInput(
                label=f"Field {field_num} Value",
                placeholder=f"field {field_num} value",
                custom_id=f"field_value_{field_num}_{bot.generate_random_string(8)}",
                min_length=1,
                max_length=35,
                required=True
            )
            self.field_values.append(field_value)
            self.add_item(field_value)


    async def callback(self, interaction: Interaction) -> None:
        """
        """
        await interaction.response.defer(ephemeral=False)

        # Get the values of the inputs from the modal
        title = self.title.value
        description = self.description.value
        field_names = [f.value for f in self.field_names]
        field_values = [f.value for f in self.field_values]

        # Create a new Embed object with the input values
        embed = Embed(
            title=title,
            description=description,
            timestamp=datetime.datetime.utcnow()
        )

        for field_name, field_value in zip(field_names, field_values):
            embed.add_field(name=field_name, value=field_value)

        if self.is_preview:
            channel = self.bot.get_channel(1045953730824130590)
        else:
            settings = get_server_settings()
            channel = self.bot.get_channel(settings["announcement_channel"])

        await channel.send(embed=embed)