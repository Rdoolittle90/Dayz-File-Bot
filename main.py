from os import getenv
import os

from src.setup import create_new_server_dir, create_new_map_dir, initial_dir_setup

from src.discord.discord_static import MyClient

from disnake import ApplicationCommandInteraction, Intents
from disnake.ext.commands import when_mentioned

from dotenv import load_dotenv
from src.discord.render_traderconfig import render_traderconfig_view
from src.discord.render_types import render_types_view

from src.discord.vendor_views import select_vendors_view



def main():
    load_dotenv()

    GUILD = int(getenv("DISCORD_GUILD"))
    
    # setup intents for bot permissions
    intents = Intents.default()
    intents.members = True
    intents.presences = True

    # disable prefix in favor of just using slash commands
    # still allows for the bot to be mentioned to invoke a command if its valid
    prefix = when_mentioned

    # this is the discord bot object
    bot = MyClient(command_prefix=prefix, intents=intents)
    

    # below are all of the commands for the bot
    # default_member_permissions=8 is the same as saying only available to admins
# ADMIN COMMANDS =========================================================================================
    @bot.slash_command(default_member_permissions=1067403561537)
    async def kill(interaction: ApplicationCommandInteraction) -> None:
        """Kill the bot 🗡️🤖 requires manual reboot"""
        await interaction.send(f"Shutdown Command sent from {interaction.author}")
        await interaction.client.close()  # Throws a RuntimeError noisey but seems to have no ill effect   #FIXME


    @bot.slash_command(default_member_permissions=1067403561537)
    async def render_types(interaction: ApplicationCommandInteraction) -> None:
        """Render the types.xml for the selected map"""
        await interaction.send(view=render_types_view(), ephemeral=True)


    @bot.slash_command(default_member_permissions=1067403561537)
    async def render_traderconfig(interaction: ApplicationCommandInteraction) -> None:
        """Render the TraderConfig.txt for the selected map"""
        await interaction.send(view=render_traderconfig_view(), ephemeral=True)


    @bot.slash_command(default_member_permissions=1067403561537)
    async def add_server(interaction: ApplicationCommandInteraction) -> None:
        """"""
        create_new_server_dir(interaction.guild.id)
        await interaction.send(f"New Directory created for {interaction.guild.name}")


    @bot.slash_command(default_member_permissions=1067403561537)
    async def add_map(interaction: ApplicationCommandInteraction, mapname: str) -> None:
        """"""
        create_new_map_dir(interaction.guild.id, mapname)
        await interaction.send(f"New Directory created for {mapname}")


    @bot.slash_command(default_member_permissions=1067403561537)
    async def remove_map(interaction: ApplicationCommandInteraction, mapname: str, passkey: int) -> None:
        """"""

        await interaction.send(f"New Directory created for {mapname}")


# @everyone COMMANDS ======================================================================================



# START THE BOT ===========================================================================================
    # start the bot loop
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
    display_title()
    if "_files" not in os.listdir():
        initial_dir_setup()
    main()