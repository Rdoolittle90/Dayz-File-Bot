﻿import os

import requests
from disnake import Color, DMChannel, Embed, Guild, Message, NotFound, SelectOption
from disnake.errors import Forbidden
from disnake.utils import get

from json import load, dump


async def initial_server_setup(guild: Guild):
    try:
        await guild.create_role(name="Bot Manager", color=Color.darker_grey())
    except:
        pass


async def initial_cha_setup(guild: Guild):
    try:
        channel = get(guild.categories, name='BOT CONTROLS')
        if channel is None:
            category = await guild.create_category("BOT CONTROLS")
            channel = await category.create_text_channel('drifter-imports')
            embed = Embed(title="How to upload a file", description="Files must be uploaded by the following commands", color=Color.blurple())
            embed.add_field(name="Step 1", value="Attach files to a message", inline=False)
            embed.add_field(name="Step 2", value="send `@Drifter map_name` as the message with the files", inline=False)
            embed.add_field(name="Step 3", value="wait for confirmation of upload.", inline=False)

            await channel.send(embed=embed)
    except Forbidden:
        print("Missing Permissions!")


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
    map_name = message.content.split(" ")[1]
    attachments = message.attachments
    await message.delete()
    if len(attachments) > 0:
        for file in attachments:
            response = requests.get(file.url)
            try:
                if file.filename.endswith(".txt"):
                    with open(f"_files/{message.guild.id}/maps/{map_name}/inputs/TraderConfig.txt", "wb") as text_out:
                        text_out.write(response.content)

                elif file.filename.endswith(".xml"):
                    with open(f"_files/{message.guild.id}/maps/{map_name}/inputs/{file.filename}", "wb") as xml_out:
                        xml_out.write(response.content)

            except FileNotFoundError:
                print("something went wrong")
                print(f"_files/{message.guild.id}/maps/{map_name}/inputs/{file.filename}")
                print("Not found")


def get_server_settings(guild_id) -> dict:
    with open(f"_files/{guild_id}/support/settings.json", "r") as json_in:
        settings = load(json_in)
    return settings


def set_announce_channel(guild: Guild, channel_id: int) -> bool:
    print(guild.name, channel_id)
    try:
        channel = guild.fetch_channel(channel_id)
    except NotFound:
        return False

    print("Found")

    settings = get_server_settings(guild.id)
    settings["announcement_channel"] = channel_id
    with open(f"_files/{guild.id}/support/settings.json", "w") as json_out:
        dump(settings, json_out, indent=4)
    return True


def get_map_selections(guild_id, type_return="SelectOption"):
    if str(guild_id) in os.listdir("_files"):
        maps = os.listdir(f"_files/{guild_id}/maps")
        selections = []
        selections_list = []
        if len(maps) > 0:
            for guild_map in maps:
                selections.append(SelectOption(label=guild_map))
                selections_list.append(guild_map)
        else:
            selections.append(SelectOption(label="No Maps Found", emoji="❌", description="This probably means no map has been setup for this server."))

        if type_return == "SelectOption":
            return selections
        else:
            return selections_list
    return None


## get player atms


## get server mods
