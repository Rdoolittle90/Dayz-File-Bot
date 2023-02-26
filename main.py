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

    # below are all of the commands for the bot
    # default_member_permissions=8 is the same as saying only available to admins

# =========================================================================================================
# ADMIN DISCORD COMMANDS ----------------------------------------------------------------------------------
# =========================================================================================================
    @bot.slash_command(default_member_permissions=8, dm_permission=False)
    async def set_status(ctx, status_code:int, map_name="ALL", message=None):
        """status_codes: 0: "OFFLINE", 1: "ONLINE", 2: "RESTARTING" """
        await announce_status(ctx, status_code, map_name, message)

    @bot.slash_command(default_member_permissions=8, dm_permission=False)
    async def set_announcement_channel(ctx, channel_id: str):
        """sets the bots announcement channel"""
        await ctx.response.defer(ephemeral=True)
        channel = await set_announce_channel(ctx.guild, int(channel_id))
        await ctx.followup.send(channel)        

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
    async def register(ctx) -> None:
        """placeholder"""
        await ctx.response.send_modal(modal=EnterSteamID())

    # =====================================================================================================
    @has_role("Steam Linked")
    @bot.slash_command(dm_permission=False, hidden=True)
    async def atm(ctx) -> None:
        """placeholder"""
        pass


    # =====================================================================================================
    @has_role("Steam Linked")
    @bot.slash_command(dm_permission=False, hidden=True)
    async def inventory(ctx) -> None:
        print(type(ctx))
        """placeholder"""
        pass


    # =====================================================================================================
    @has_role("Steam Linked")
    @bot.slash_command(dm_permission=False, hidden=True)
    async def trade(ctx) -> None:
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