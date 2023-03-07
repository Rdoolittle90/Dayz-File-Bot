import os

from dotenv import load_dotenv
from nextcord.ext import tasks
from src.helpers.divider_title import divider_title

from src.discord.bot import DiscordBot
from src.discord.guild_manager import initial_cha_setup, initial_server_setup
from src.file_manager import create_new_server_dir, initial_dir_setup
from src.ftp.ftp_manager import FTPConnect
from src.helpers.colored_printing import colorized_print
from src.http.requester import CFTools
from src.sql.sql_manager import DBConnect

DEBUG_LEVEL = "DEBUG"

def main():
    load_dotenv()
    # this is the discord bot object
    bot:DiscordBot = DiscordBot()

    wait_until_ready.start(bot)
    bot.run(os.getenv("DISCORD_TOKEN"))



@tasks.loop(count=1)
async def wait_until_ready(bot: DiscordBot):
    colorized_print("DEBUG", "Waiting until ready.")
    await bot.wait_until_ready()
    colorized_print("DEBUG", "Ready.")
    initial_dir_setup()
    for guild in bot.guilds:
        colorized_print("GUILD", f"{guild.name}")
        await initial_cha_setup(guild)
        await initial_server_setup(guild)
        create_new_server_dir()
    divider_title("Begin Log", bot.width, bot.secondary_symbol)
    bot.sql = DBConnect()
    await bot.sql.sql_connect()

    bot.ftp = FTPConnect()

    bot.cftools = CFTools()

    
if __name__ == "__main__":   
    main()