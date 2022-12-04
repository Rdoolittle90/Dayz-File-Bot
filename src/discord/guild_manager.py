import os
from disnake import SelectOption



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
