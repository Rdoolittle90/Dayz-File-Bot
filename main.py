import os
import asyncio
from dotenv import load_dotenv
from nextcord.ext import tasks
from src.helpers.divider_title import divider_title
from src.discord.bot import DiscordBot
from src.discord.guild_manager import initial_cha_setup, initial_server_setup
from src.file_manager import create_new_server_dir, initial_dir_setup
from src.helpers.colored_printing import colorized_print


async def setup_guild(bot: DiscordBot, guild):
    try:
        colorized_print("GUILD", f"{guild.name}")
        await initial_cha_setup(guild)
        await initial_server_setup(guild)
        create_new_server_dir()
    except Exception as e:
        colorized_print("ERROR", f"Error setting up guild {guild.name}: {e}")


async def setup(bot: DiscordBot):
    colorized_print("DEBUG", "Ready.")
    bot.display_title()
    initial_dir_setup()
    divider_title("Guilds", bot.width, bot.secondary_symbol)
    await asyncio.gather(*[setup_guild(bot, guild) for guild in bot.guilds])
    await bot.setup()
    divider_title("Begin Log", bot.width, bot.secondary_symbol)


@tasks.loop(count=1)
async def wait_until_ready(bot: DiscordBot):
    colorized_print("DEBUG", "Waiting until ready.")
    await bot.wait_until_ready()
    await setup(bot)


def main():
    load_dotenv()
    bot = DiscordBot()
    wait_until_ready.start(bot)
    bot.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()