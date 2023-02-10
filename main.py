from os import getenv
import os

from disnake import ApplicationCommandInteraction, Embed, Intents, Message, Color
from disnake.ext.commands import when_mentioned
from dotenv import load_dotenv
from src.ftp.ftp_manager import FTPConnect
from src.sql.sql_manager import DBConnect
from src.dayz.atm_manager import display_player_atm, update_player_atm
from src.discord.modals.registration import Registration
from src.discord.guild_manager import set_announce_channel
from src.discord.announcements import announce_status

from src.discord.bot import MyClient
from src.discord.guild_manager import get_map_selections
from src.discord.load_traderconfig import load_traderconfig_view
from src.discord.load_types import load_types_view
from src.discord.modals.remove_map_modal import RemoveMapModal
from src.discord.render_traderconfig import render_traderconfig_view
from src.discord.render_types import render_types_view
from src.file_manager import create_new_map_dir, get_map_key, key_embed


def main():
    load_dotenv()

    # setup intents for bot permissions
    intents = Intents.default()
    intents.message_content = True

    # disable prefix in favor of just using slash commands
    # still allows for the bot to be mentioned to invoke a command if its valid
    prefix = when_mentioned

    # this is the discord bot object
    bot = MyClient(command_prefix=prefix, intents=intents)


    # below are all of the commands for the bot
    # default_member_permissions=8 is the same as saying only available to admins

# =========================================================================================================
# ADMIN DISCORD COMMANDS ----------------------------------------------------------------------------------
# =========================================================================================================
    @bot.slash_command(default_member_permissions=1067403561537, dm_permission=False)
    async def set_status(interaction: ApplicationCommandInteraction, status_code:int, map_name="ALL", message=None):
        """status_codes: 0: "OFFLINE", 1: "ONLINE", 2: "RESTARTING" """
        await announce_status(interaction, status_code, map_name, message)

    @bot.slash_command(default_member_permissions=1067403561537, dm_permission=False)
    async def set_announcement_channel(interaction: ApplicationCommandInteraction, channel_id: str):
        """sets the bots announcement channel"""
        await interaction.response.defer(ephemeral=True)
        channel = await set_announce_channel(interaction.guild, int(channel_id))
        await interaction.followup.send(channel)

    @bot.slash_command(default_member_permissions=1067403561537, dm_permission=False)
    async def clean_bot_chatter(interaction: ApplicationCommandInteraction, channel_id: str):
        """deletes messages at given channel from the bot"""
        channel = bot.get_channel(int(channel_id))
        await interaction.send(f"deleting the messages I have sent in #{channel.name}")
        

# =========================================================================================================
# ADMIN FILE COMMANDS -------------------------------------------------------------------------------------
# =========================================================================================================
    @bot.slash_command(default_member_permissions=1067403561537, dm_permission=False)
    async def add_map(interaction:ApplicationCommandInteraction, mapname: str) -> None:
        """creates a new map directory"""
        create_new_map_dir(interaction.guild.id, mapname)
        await interaction.send(f"New Directory created for {mapname}")

    # =====================================================================================================
    @bot.slash_command(default_member_permissions=1067403561537, dm_permission=False)
    async def render_types(interaction:ApplicationCommandInteraction) -> None:
        """Render the types.xml for the selected map"""
        options = get_map_selections(interaction.guild.id)
        if options:
            await interaction.send(view=render_types_view(options=options), ephemeral=True)
        else:
            await interaction.send("Server has no registered maps", ephemeral=True)

    # =====================================================================================================
    @bot.slash_command(default_member_permissions=1067403561537, dm_permission=False)
    async def render_traderconfig(interaction: ApplicationCommandInteraction) -> None:
        """Render the TraderConfig.txt for the selected map"""
        options = get_map_selections(interaction.guild.id)
        if options:
            await interaction.send(view=render_traderconfig_view(options=options), ephemeral=True)
        else:
            await interaction.send("Server has no registered maps", ephemeral=True)

    # =====================================================================================================
    @bot.slash_command(default_member_permissions=1067403561537, dm_permission=False)
    async def load_traderconfig(interaction: ApplicationCommandInteraction) -> None:
        """Render the TraderConfig.txt for the selected map"""
        options = get_map_selections(interaction.guild.id)
        if options:
            await interaction.send(view=load_traderconfig_view(options=options), ephemeral=True)
        else:
            await interaction.send("Server has no registered maps", ephemeral=True)

    # =====================================================================================================
    @bot.slash_command(default_member_permissions=1067403561537, dm_permission=False)
    async def load_types(interaction: ApplicationCommandInteraction) -> None:
        """Render the TraderConfig.txt for the selected map"""
        options = get_map_selections(interaction.guild.id)
        if options:
            await interaction.send(view=load_types_view(options=options), ephemeral=True)
        else:
            await interaction.send("Server has no registered maps", ephemeral=True)

    # =====================================================================================================
    @bot.slash_command(default_member_permissions=1067403561537, dm_permission=False)
    async def kill(interaction:ApplicationCommandInteraction) -> None:
        """Kill the bot 🗡️🤖 requires manual reboot"""
        await interaction.send(f"Shutdown Command sent from {interaction.author}")
        await interaction.client.close()  # Throws a RuntimeError noisey but seems to have no ill effect   #FIXME


    # =====================================================================================================
    @bot.slash_command(default_member_permissions=1067403561537, dm_permission=False)
    async def get_key(interaction:ApplicationCommandInteraction, mapname: str) -> None:
        """Looks up the given maps passkey"""
        passkey = get_map_key(interaction.guild.id, mapname)["passkey"]
        await interaction.send(embed=key_embed(mapname, passkey))


    # =====================================================================================================
    @bot.slash_command(default_member_permissions=1067403561537, dm_permission=False)
    async def remove_map(interaction:ApplicationCommandInteraction) -> None:
        """Opens the map deletion Modal"""
        await interaction.response.send_modal(modal=RemoveMapModal())


    # =====================================================================================================
    @bot.slash_command(default_member_permissions=1067403561537, dm_permission=False)
    async def get_all_atms(interaction:ApplicationCommandInteraction) -> None:
        await interaction.response.defer()
        sql = DBConnect()
        sql_cmmd = "INSERT IGNORE INTO registration (SK64) VALUES (%s)"

        for folder_name in os.listdir("_files\919677581824000070\maps"):
            print(folder_name)
            ftp = FTPConnect(folder_name)
            ftp.connect()
            ftp.getAllPlayerATM(919677581824000070)
            for file_name in os.listdir(f"_files\919677581824000070\maps\{folder_name}\\atms"):
                sql.c.execute(sql_cmmd, (file_name.strip(".json"), ))
            sql.commit()
            ftp.ftp.close()
        sql.close()
        await interaction.followup.send("Done!")



    # =====================================================================================================
    @bot.slash_command(default_member_permissions=1067403561537, dm_permission=False)
    async def give_money(interaction:ApplicationCommandInteraction, steamid64, map_num:int, amount:int) -> None:
        """map_nums = Chernarus:0, Takistan:1, Namalsk:2, testServer:3"""
        maps = ["Chernarus", "Takistan", "Namalsk", "TestServer"]
        await interaction.response.defer()
        update_player_atm(maps[map_num], interaction.author.id, amount, SK64=steamid64)
        embed: Embed
        message: Message
        embed, message = await display_player_atm(interaction, interaction.author.id)

        if amount >= 0:
            amount_str = "+" + f"{amount:,} ₽"
            embed.color = Color.green()
        else:
            amount_str = f"{amount:,}₽"
            embed.color = Color.red()

        embed.add_field(name=f"Cash given by: {interaction.author.display_name}", value=amount_str)
        await message.edit(embed=embed)

# =========================================================================================================
# @everyone COMMANDS --------------------------------------------------------------------------------------
# =========================================================================================================
    @bot.slash_command(dm_permission=False)
    async def register(interaction:ApplicationCommandInteraction) -> None:
        """placeholder"""
        await interaction.response.send_modal(modal=Registration())


    # =====================================================================================================
    @bot.slash_command(dm_permission=False)
    async def atm(interaction:ApplicationCommandInteraction) -> None:
        """placeholder"""
        await interaction.response.defer()
        await display_player_atm(interaction, interaction.author.id)


    # =====================================================================================================
    @bot.slash_command(dm_permission=False)
    async def inventory(interaction:ApplicationCommandInteraction) -> None:
        """placeholder"""
        pass


    # =====================================================================================================
    @bot.slash_command(dm_permission=False)
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
    display_title()        
    main()