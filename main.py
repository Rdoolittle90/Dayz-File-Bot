from os import getenv

from nextcord import ApplicationCommandInteraction, Intents
from nextcord.ext.commands import when_mentioned, has_role
from dotenv import load_dotenv

from src.discord.announcements import announce_status
from src.discord.bot import DiscordBot
from src.discord.guild_manager import set_announce_channel
from src.discord.registration import EnterSteamID




def main():
    load_dotenv()
    display_title()     

    # setup intents for bot permissions
    intents = Intents.default()
    intents.message_content = True

    # disable prefix in favor of just using slash commands
    # still allows for the bot to be mentioned to invoke a command if its valid
    prefix = when_mentioned

    # this is the discord bot object
    bot = DiscordBot(command_prefix=prefix, intents=intents)
    bot.openai_api_key = "api_key_here"

    # below are all of the commands for the bot
    # default_member_permissions=8 is the same as saying only available to admins

# =========================================================================================================
# ADMIN DISCORD COMMANDS ----------------------------------------------------------------------------------
# =========================================================================================================
    @bot.slash_command(default_member_permissions=8, dm_permission=False)
    async def set_status(interaction: ApplicationCommandInteraction, status_code:int, map_name="ALL", message=None):
        """status_codes: 0: "OFFLINE", 1: "ONLINE", 2: "RESTARTING" """
        await announce_status(interaction, status_code, map_name, message)

    @bot.slash_command(default_member_permissions=8, dm_permission=False)
    async def set_announcement_channel(interaction: ApplicationCommandInteraction, channel_id: str):
        """sets the bots announcement channel"""
        await interaction.response.defer(ephemeral=True)
        channel = await set_announce_channel(interaction.guild, int(channel_id))
        await interaction.followup.send(channel)        

# =========================================================================================================
# ADMIN FILE COMMANDS -------------------------------------------------------------------------------------
# =========================================================================================================

    bot.load_extension("src.discord.cogs.admin_commands")
    # bot.load_extension("src/discord/cogs/everyone_commands")
    # bot.load_extension("src/discord/cogs/registered_commands")


# =========================================================================================================
# @everyone COMMANDS --------------------------------------------------------------------------------------
# =========================================================================================================
    @bot.slash_command(dm_permission=False)
    async def register(interaction:ApplicationCommandInteraction) -> None:
        """placeholder"""
        await interaction.response.send_modal(modal=EnterSteamID())

    # =====================================================================================================
    @has_role("Steam Linked")
    @bot.slash_command(dm_permission=False, hidden=True)
    async def atm(interaction:ApplicationCommandInteraction) -> None:
        """placeholder"""
        pass


    # =====================================================================================================
    @has_role("Steam Linked")
    @bot.slash_command(dm_permission=False, hidden=True)
    async def inventory(interaction:ApplicationCommandInteraction) -> None:
        """placeholder"""
        pass


    # =====================================================================================================
    @has_role("Steam Linked")
    @bot.slash_command(dm_permission=False, hidden=True)
    async def trade(interaction:ApplicationCommandInteraction) -> None:
        """placeholder"""
        pass

# =========================================================================================================
# START THE BOT |=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|
# =========================================================================================================
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