import os
from disnake import SelectOption



def get_map_selections(guild_id) -> list[SelectOption] | None:
    if guild_id in os.listdir("_files"):
        maps = os.listdir(f"_files/{guild_id}/maps")
        if len(maps) > 0:
            selections = []
            for guild_map in maps:
                selections.append(SelectOption(label=guild_map))
        else:
            selections.append(SelectOption(label="No Maps Found", emoji="❌", discription="This probably means no map has been setup for this server."))

        return selections

    return None