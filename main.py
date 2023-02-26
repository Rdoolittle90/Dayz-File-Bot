from os import getenv
from nextcord.ext.commands import has_role
from dotenv import load_dotenv

from src.discord.announcements import announce_status
from src.discord.bot import DiscordBot
from src.discord.guild_manager import set_announce_channel
from src.discord.registration import EnterSteamID




def main():
    load_dotenv()
    display_title()     

    # this is the discord bot object
    bot = DiscordBot()
    bot.openai_api_key = "api_key_here"

    bot.load_extension("src.discord.cogs.admin_commands")
    bot.load_extension("src/discord/cogs/registered_commands")
    # bot.load_extension("src/discord/cogs/everyone_commands")


    bot.run(getenv("DISCORD_TOKEN"))


def display_title():
    name = getenv("APP_NAME")
    version = getenv("APP_VERSION")
    app_title = f" {name} Discord Bot  v.{version} "
    app_display = f"""
{'=' * (len(app_title) + 8)}
    {app_title}
{'=' * (len(app_title) + 8)}
"""
    print(app_display)



# =========================================================================================================
# =========================================================================================================
# =========================================================================================================
if __name__ == "__main__":   
    main()