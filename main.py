import logging
import os
from logging import Logger

from dotenv import load_dotenv
from nextcord.ext import tasks

from src.discord.bot import DiscordBot
from src.discord.guild_manager import initial_cha_setup, initial_server_setup
from src.ftp.ftp_manager import FTPConnect
from src.file_manager import create_new_server_dir, initial_dir_setup
from src.helpers.colored_logging import colorize_log
from src.sql.sql_manager import DBConnect



logger = Logger(__name__)
logger.setLevel(logging.INFO)

def main():
    load_dotenv()
    # this is the discord bot object
    bot:DiscordBot = DiscordBot()

    wait_until_ready.start(bot)
    bot.run(os.getenv("DISCORD_TOKEN"))



@tasks.loop(count=1)
async def wait_until_ready(bot: DiscordBot):
    colorize_log("DEBUG", "Waiting until ready.")
    await bot.wait_until_ready()
    colorize_log("DEBUG", "Ready.")
    initial_dir_setup()
    for guild in bot.guilds:
        colorize_log("INFO", f"Connected to: {guild.name}")
        await initial_cha_setup(guild)
        await initial_server_setup(guild)
        create_new_server_dir()

    print(bot.app_display_secondary)
    bot.sql = DBConnect()
    await bot.sql.sql_connect()

    bot.ftp = FTPConnect()

    
if __name__ == "__main__":   
    main()