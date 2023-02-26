from os import getenv

from disnake import ApplicationCommandInteraction, Intents
from disnake.ext.commands import when_mentioned, has_role, MissingRole, CommandNotFound
from dotenv import load_dotenv

from src.discord.announcements import announce_status
from src.discord.bot import DiscordBot
from src.discord.guild_manager import get_map_selections, set_announce_channel
from src.discord.load_traderconfig import load_traderconfig_view
from src.discord.modals.remove_map_modal import RemoveMapModal
from src.discord.registration import EnterSteamID
from src.file_manager import create_new_map_dir, get_map_key, key_embed




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
    @bot.slash_command(dm_permission=False)
    async def add_map(interaction:ApplicationCommandInteraction, mapname: str) -> None:
        """creates a new map directory"""
        create_new_map_dir(interaction.guild.id, mapname)
        await interaction.send(f"New Directory created for {mapname}")

    # =====================================================================================================
    @bot.slash_command(default_member_permissions=8, dm_permission=False)
    async def load_traderconfig(interaction: ApplicationCommandInteraction) -> None:
        """Render the TraderConfig.txt for the selected map"""
        options = get_map_selections(interaction.guild.id)
        if options:
            await interaction.send(view=load_traderconfig_view(options=options), ephemeral=True)
        else:
            await interaction.send("Server has no registered maps", ephemeral=True)

    # =====================================================================================================
    @bot.slash_command(default_member_permissions=8, dm_permission=False)
    async def kill(interaction:ApplicationCommandInteraction) -> None:
        """Kill the bot 🗡️🤖 requires manual reboot"""
        await interaction.send(f"Shutdown Command sent from {interaction.author}")
        await bot.pool.close()
        await interaction.client.close()  # Throws a RuntimeError noisey but seems to have no ill effect   #FIXME


    # =====================================================================================================
    @bot.slash_command(default_member_permissions=8, dm_permission=False)
    async def get_key(interaction:ApplicationCommandInteraction, mapname: str) -> None:
        """Looks up the given maps passkey"""
        passkey = get_map_key(interaction.guild.id, mapname)["passkey"]
        await interaction.send(embed=key_embed(mapname, passkey))


    # =====================================================================================================
    @bot.slash_command(default_member_permissions=8, dm_permission=False)
    async def remove_map(interaction:ApplicationCommandInteraction) -> None:
        """Opens the map deletion Modal"""
        await interaction.response.send_modal(modal=RemoveMapModal())

# =========================================================================================================
# @everyone COMMANDS --------------------------------------------------------------------------------------
# =========================================================================================================
    @bot.slash_command(dm_permission=False)
    async def register(interaction:ApplicationCommandInteraction) -> None:
        """placeholder"""
        await interaction.response.send_modal(modal=EnterSteamID())

    # =====================================================================================================
    @bot.slash_command(dm_permission=False, hidden=True)
    @has_role("Steam Linked")
    async def atm(interaction:ApplicationCommandInteraction) -> None:
        """placeholder"""
        pass


    # =====================================================================================================
    @bot.slash_command(dm_permission=False, hidden=True)
    @has_role("Steam Linked")
    async def inventory(interaction:ApplicationCommandInteraction) -> None:
        """placeholder"""
        pass


    # =====================================================================================================
    @bot.slash_command(dm_permission=False, hidden=True)
    @has_role("Steam Linked")
    async def trade(interaction:ApplicationCommandInteraction) -> None:
        """placeholder"""
        pass

# =========================================================================================================
# START THE BOT |=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|
# =========================================================================================================



    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, MissingRole):
            await ctx.send(f"Error: {error}")
            return
        elif isinstance(error, CommandNotFound):
            # Handle CommandNotFound error
            return
        # Handle other types of errors
    

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