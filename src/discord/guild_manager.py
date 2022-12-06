import os
from disnake import Color, Embed, Guild, SelectOption
from disnake.errors import Forbidden
from disnake.utils import get


async def initial_cha_setup(guild: Guild):
    try:
        channel = get(guild.categories, name='BOT CONTROLS')
        if channel is None:
            category = await guild.create_category("BOT CONTROLS")
            channel = await category.create_text_channel('drifter-imports')
            embed = Embed(title="How to upload a file", description="Files must be uploaded by the following commands", color=Color.blurple())
            embed.add_field(name="Step 1", value="Attach files to a message")
            embed.add_field(name="Step 2", value="send `@Drifter map_name` as the message with the files")
            embed.add_field(name="Step 3", value="wait for confirmation of upload.")

            await channel.send(embed=embed)
    except Forbidden:
        print("Missing Permissions!")



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
            selections.append(SelectOption(label="No Maps Found", emoji="❌", discription="This probably means no map has been setup for this server."))

        if type_return == "SelectOption":
            return selections
        else:
            return selections_list
    return None


## get player atms


## get server mods
