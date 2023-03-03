from os import getenv
from dotenv import load_dotenv

from src.discord.bot import DiscordBot




def main():
    load_dotenv()
    display_title()     

    # this is the discord bot object
    bot = DiscordBot()

    # bot.load_extension("src.discord.cogs.admin_commands")
    bot.load_extension("src.discord.cogs.core_commands")
    bot.load_extension("src.discord.cogs.dayz_admin_commands")
    bot.load_extension("src.discord.cogs.dayz_user_commands")
    bot.load_extension("src.discord.cogs.minigame_commands")
    # bot.load_extension("src.discord.cogs.everyone_commands")
    # bot.load_extension("src.discord.cogs.test_commands")

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

    
if __name__ == "__main__":   
    main()