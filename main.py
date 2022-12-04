import os
from os import getenv

from disnake import ApplicationCommandInteraction, Intents
from disnake.ext.commands import when_mentioned
from dotenv import load_dotenv

from src.discord.discord_static import MyClient
from src.discord.guild_manager import get_map_selections
from src.discord.modals.remove_map_modal import RemoveMapModal
from src.discord.render_traderconfig import render_traderconfig_view
from src.discord.render_types import render_types_view
from src.file_manager import (create_new_map_dir, create_new_server_dir,
                              get_map_key, initial_dir_setup, key_embed)


def main():
    load_dotenv()
        
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
    async def add_map(interaction:ApplicationCommandInteraction, mapname: str) -> None:
        """creates a new map directory"""
        create_new_map_dir(interaction.guild.id, mapname)
        await interaction.send(f"New Directory created for {mapname}")


    @bot.slash_command(default_member_permissions=1067403561537)
    async def render_types(interaction:ApplicationCommandInteraction) -> None:
        """Render the types.xml for the selected map"""
        options = get_map_selections(interaction.guild.id)
        if options:
            await interaction.send(view=render_types_view(options=options), ephemeral=True)
        else:
            await interaction.send("Server has no registered maps", ephemeral=True)


    @bot.slash_command(default_member_permissions=1067403561537)
    async def render_traderconfig(interaction: ApplicationCommandInteraction) -> None:
        """Render the TraderConfig.txt for the selected map"""
        options = get_map_selections(interaction.guild.id)
        if options:
            await interaction.send(view=render_traderconfig_view(options=options), ephemeral=True)
        else:
            await interaction.send("Server has no registered maps", ephemeral=True)


    @bot.slash_command(default_member_permissions=1067403561537)
    async def kill(interaction:ApplicationCommandInteraction) -> None:
        """Kill the bot 🗡️🤖 requires manual reboot"""
        await interaction.send(f"Shutdown Command sent from {interaction.author}")
        await interaction.client.close()  # Throws a RuntimeError noisey but seems to have no ill effect   #FIXME


    @bot.slash_command(default_member_permissions=1067403561537)
    async def get_key(interaction:ApplicationCommandInteraction, mapname: str) -> None:
        """Looks up the given maps passkey"""
        passkey = get_map_key(interaction.guild.id, mapname)["passkey"]
        await interaction.send(embed=key_embed(mapname, passkey))


    @bot.slash_command(default_member_permissions=1067403561537)
    async def remove_map(interaction:ApplicationCommandInteraction) -> None:
        """Opens the map deletion Modal"""
        await interaction.response.send_modal(modal=RemoveMapModal())


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
    main()