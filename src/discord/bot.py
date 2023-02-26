from disnake import Member
from disnake.ext.commands import Bot
from disnake.message import Message
import logging
from src.sql.sql_manager import DBConnect
from src.discord.guild_manager import check_for_files, initial_cha_setup, initial_server_setup
from src.file_manager import create_new_server_dir, initial_dir_setup


class DiscordBot(Bot, DBConnect):
    """
    Custom bot class inheriting from the `discord.ext.commands.Bot` class and the `DBConnect` mixin.

    This class handles the bot's events and has methods for setting up the server directories and channels
    upon initialization, as well as handling messages and member join/leave events.

    Args:
        Bot (discord.ext.commands.Bot): The bot object to handle Discord events.
        DBConnect (mixin): A mixin class that defines a `sql_connect` method for connecting to a database.

    Attributes:
        (None)

    """

    async def on_ready(self) -> None:
        """
        Event handler for the `on_ready` event.

        This method is called when the bot is ready to start handling events. It initializes the directory
        structure for the server and sets up the necessary channels.

        Args:
            (None)

        Returns:
            (None)

        """
        initial_dir_setup()
        for guild in self.guilds:
            await initial_cha_setup(guild)
            await initial_server_setup(guild)
            create_new_server_dir()
        await self.sql_connect()

    async def on_message(self, message: Message) -> None:
        """
        Event handler for the `on_message` event.

        This method is called when a message is sent in a server where the bot is present. It checks the
        message for any attachments and saves them to disk.

        Args:
            message (discord.Message): The message object containing the message content and attachments.

        Returns:
            (None)

        """
        if message.author != self.user:
            await check_for_files(message)

    async def on_member_join(self, member: Member) -> None:
        """
        Event handler for the `on_member_join` event.

        This method is called when a new member joins the server. It logs the event to the console.

        Args:
            member (discord.Member): The member object representing the new member.

        Returns:
            (None)

        """
        logging.info(f'{member.name} has joined the server')

    async def on_member_remove(self, member: Member) -> None:
        """
        Event handler for the `on_member_remove` event.

        This method is called when a member leaves the server. It logs the event to the console.

        Args:
            member (discord.Member): The member object representing the departing member.

        Returns:
            (None)

        """
        logging.info(f'{member.name} has left the server')