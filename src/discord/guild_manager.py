import os
from json import dump, load

import requests
from nextcord import (CategoryChannel, Colour, DMChannel, Embed, File, Guild,
                      Message, NotFound, SelectOption, TextChannel, Role)
from nextcord.errors import Forbidden
from nextcord.utils import get

from src.helpers.colored_logging import colorize_log


async def initial_server_setup(guild: Guild):
    try:
        bot_manager_role = get(guild.roles, name='Bot Manager')
        if bot_manager_role is None:
            new_role: Role = await guild.create_role(name="Bot Manager", color=Colour.darker_grey())
            colorize_log("DEBUG", f"Created new role {new_role.name} in guild {guild.name}")
        else:
            colorize_log("DEBUG", f"Found Role {bot_manager_role.name} in guild {guild.name}")

    except Forbidden:
        colorize_log("ERROR", "Missing Permissions!")


async def initial_cha_setup(guild: Guild):
    try:
        category: CategoryChannel = get(guild.categories, name='BOT CONTROLS')
        channel: TextChannel = get(guild.channels, name='drifter-imports')
        if category is None:
            category = await guild.create_category("BOT CONTROLS")
            channel = await category.create_text_channel('drifter-imports')
            embed = Embed(title="How to upload a file", description="Files must be uploaded by the following commands", color=Colour.blurple())
            embed.add_field(name="Step 1", value="Attach files to a message", inline=False)
            embed.add_field(name="Step 2", value="send `@Drifter map_name` as the message with the files", inline=False)
            embed.add_field(name="Step 3", value="wait for confirmation of upload.", inline=False)
            await channel.send(embed=embed)
            colorize_log("DEBUG", f"Created new text channel in category {category.name}")
        else:
            colorize_log("DEBUG", f"Found text channel {channel.name} in category {channel.category.name} in guild {guild.name}")
    except Forbidden:
        colorize_log("ERROR", "Missing Permissions!")


async def check_for_files(message: Message):
    """"""     
    if isinstance(message.channel, DMChannel):
        return
    if message.channel.name != "drifter-imports":
        return
    if len(message.content) == 0:
        return
    if message == None:
        return


    map_name = message.content
    attachments = message.attachments
    await message.delete()
    if len(attachments) == 0:
        return


    for _file in attachments:
        store_attachment(_file, message.guild.id, map_name)



def store_attachment(file: File, guild_id, map_name):
    if not os.path.exists(f"_files/{guild_id}/maps/{map_name}"):
        print("something went wrong")
        print(f"_files/{guild_id}/maps/{map_name}/inputs/{file.filename}")
        print("Not found")
        return

    response = requests.get(file.url)
    if file.filename.endswith(".txt"):
        with open(f"_files/{guild_id}/maps/{map_name}/inputs/TraderConfig.txt", "wb") as text_out:
            text_out.write(response.content)

    elif file.filename.endswith(".xml"):
        with open(f"_files/{guild_id}/maps/{map_name}/inputs/{file.filename}", "wb") as xml_out:
            xml_out.write(response.content)


def get_server_settings() -> dict:
    with open(f"_files/support/settings.json", "r") as json_in:
        settings = load(json_in)
    return settings


async def set_announce_channel(guild: Guild, channel_id: int) -> bool:
    print(guild.name, channel_id)
    try:
        channel = await guild.fetch_channel(channel_id)
    except NotFound:
        return False

    print("Found")

    settings = get_server_settings()
    settings["announcement_channel"] = channel_id
    with open(f"_files/support/settings.json", "w") as json_out:
        dump(settings, json_out, indent=4)
    return True


def get_map_selections(type_return="SelectOption"):
    if not os.path.exists(f"_files"):
        return None
        
    maps = os.listdir(f"_files/maps")
    selections = []
    selections_list = []
    if len(maps) == 0:
        selections.append(SelectOption(label="No Maps Found", emoji="❌", description="This probably means no map has been setup for this server."))
        return None

    for guild_map in maps:
        selections.append(SelectOption(label=guild_map))
        selections_list.append(guild_map)
        
    if type_return == "SelectOption":
        return selections
    else:
        return selections_list
