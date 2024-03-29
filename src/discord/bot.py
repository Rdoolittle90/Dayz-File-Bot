"""
This module contains a custom Discord bot class `DiscordBot`, 
which handles events and sets up server directories and channels upon initialization.
It also defines event handlers for member join/leave events and message events.

Classes:
- DiscordBot:
    A custom bot class that inherits from the `nextcord.ext.commands.Bot` class 
    and the `DBConnect` mixin.

Functions:
- generate_random_string(length): Returns a random string of the given length.

Event Handlers:
- on_ready: Initializes the directory structure for the server and sets up the necessary channels.
- on_message: Checks the message for any attachments and saves them to disk.
- on_member_join: Logs when a new member joins the server.
- on_member_remove: Logs when a member leaves the server.

Attributes:
- cftools: An instance of the `CFTools` class.
- ftp: An instance of the `FTPConnect` class.
- sql: An instance of the `DBConnect` class.
"""


import asyncio
import datetime
import json
import logging
import os
from typing import Dict

from colorama import Fore, Style
from nextcord import Intents, Member, Message
from nextcord.ext import commands

from src.discord.guild_manager import check_for_files
from src.ftp.ftp_manager import FTPConnect
from src.helpers.colored_printing import colorized_print
from src.helpers.divider_title import divider_title
from src.http.cftools import CFTools
from src.sql.sql_manager import DBConnect


class DiscordBot(commands.Bot):
    """
    Custom bot class inheriting from the `nextcord.ext.commands.Bot` class and the `DBConnect` mixin

    This class handles the bot's events and has methods for setting up the server directories 
    and channels upon initialization, as well as handling messages and member join/leave events.

    Args:
        Bot (nextcord.ext.commands.Bot): The bot object to handle Discord events.
        DBConnect (mixin): 
            A mixin class that defines a `sql_connect` method for connecting to a database.

    Attributes:
        (None)
    """

    intents = Intents.default()
    intents.message_content = True
    intents.members = True
    prefix = commands.when_mentioned

    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=DiscordBot.prefix, intents=DiscordBot.intents, *args, **kwargs)
        # setup intents for bot permissions
        self.name = os.getenv("APP_NAME")
        self.version = os.getenv("APP_VERSION")
        self.app_title = f"{self.name} Discord Bot v.{self.version}"
        self.width = len(self.app_title) + 8
        self.primary_symbol = "="
        self.secondary_symbol = "-"
        self.settings = None
        
        self.add_listener(self.on_ready)
        self.add_listener(self.on_member_join)
        self.add_listener(self.on_member_remove)
        self.add_listener(self.on_message)
        self.add_listener(self.on_command_error)

        divider_title("Cogs", self.width, self.secondary_symbol)
        self.load_cogs()


    async def setup(self):
        start_time = datetime.datetime.now()

        divider_title("Connections", self.width, self.secondary_symbol)
        self.cftools: CFTools = CFTools()


        # self.ftp_connections: Dict[str, FTPConnect] = {
        #     "Chernarus": FTPConnect("Chernarus")
        # }

        # self.sql: DBConnect = DBConnect()
        # await self.sql.sql_connect()
        
        end_time = datetime.datetime.now()
        time_taken = (end_time - start_time).total_seconds() * 1000
        colorized_print("DEBUG", f"Time taken to setup: {time_taken:.2f}ms")



    async def on_ready(self) -> None:
        """
        Event handler for the `on_ready` event.

        This method is called when the bot is ready to start handling events.
        It initializes the directory structure for the server and sets up the necessary channels.

        Args:
            (None)

        Returns:
            (None)

        """
        pass


    async def on_message(self, message: Message) -> None:
        """
        Event handler for the `on_message` event.

        This method is called when a message is sent in a server where the bot is present. 
        It checks the message for any attachments and saves them to disk.

        Args:
            message (Message): The message object containing the message content and attachments.

        Returns:
            (None)

        """
        if message.author != self.user:
            logging.info(f'{Fore.RED}[LOG] checking for files from %s{Style.RESET_ALL}', message.author.name)
            await check_for_files(message)


    async def on_member_join(self, member: Member) -> None:
        logging.info('%s has joined the server', member.name)
        """
        Event handler for the `on_member_join` event.

        This method is called when a new member joins the server. It logs the event to the console.

        Args:
            member (nextcord.Member): The member object representing the new member.

        Returns:
            (None)

        """


    async def on_member_remove(self, member: Member) -> None:
        logging.info('%s has left the server', member.name)
        """
        Event handler for the `on_member_remove` event.

        This method is called when a member leaves the server. It logs the event to the console.

        Args:
            member (nextcord.Member): The member object representing the departing member.

        Returns:
            (None)

        """


    def display_title(self):
        print()
        divider_title("", self.width, self.primary_symbol)
        divider_title(self.app_title, self.width, " ")
        divider_title("", self.width, self.primary_symbol)


    def load_cogs(self):
        with open("_files/support/settings.json", "r") as json_in:
            data = json.load(json_in)

        all_extensions = [i.removesuffix(".py") for i in os.listdir("src/discord/cogs") if i.endswith(".py")]
        for extension in all_extensions:
            if extension in data["active_cogs"]:
                try:
                    self.load_extension(f"src.discord.cogs.{extension}")
                    colorized_print("COG", f"🟢 {extension.removesuffix('_commands').title()}")
                except commands.errors.ExtensionFailed:
                    colorized_print("COG", f"🔴 {extension.removesuffix('_commands').title()}  [ExtensionFailed]")
                except commands.errors.NoEntryPointError:
                    colorized_print("COG", f"🔴 {extension.removesuffix('_commands').title()}  [NoEntryPointError]")
            else:
                colorized_print("COG", f"⚫ {extension.removesuffix('_commands').title()}  [Disabled]")


    def get_settings_json(self):
        with open("_files/support/settings.json", "r") as json_in:
            self.settings = json.load(json_in)
        return self.settings


    def update_settings_file(self):
        with open("_files/support/settings.json", "w") as json_out:
            json.dump(self.settings, json_out, indent=4)


    async def my_background_task(self):
        """placeholder"""
        colorized_print("INFO", f"Starting ...")
        while not self.is_closed():
            tasks = [
                asyncio.create_task(self.ftp_connections["Chernarus"].download_all_map_atm_files_async())
            ]
            await asyncio.wait(tasks)
            await asyncio.sleep(60 * 60)  # task runs every 60 * 5 seconds

    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(f'Error: {error}')