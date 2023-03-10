import datetime
from nextcord import Embed, Color

def get_title_emoji(idx):
    if idx == 0:
        return "🥇"
    elif idx == 1:
        return "🥈"
    elif idx == 2:
        return "🥉"
    else:
        return ""


def single_map_leaderboard_embed(map_name:str, map_data: list):
    embed = Embed(title="Leaderboard", description=f'Top {len(map_data)} Players with a positive K/D', timestamp=datetime.datetime.now(), color=Color.blurple())
    field_str = ""
    map_str_name = f"**{map_name}**"
    for idx, player in enumerate(map_data):
            name = "{:24}".format(f"{get_title_emoji(idx)} `{player[0]}` {get_title_emoji(idx)}")
            kills = "{:03}".format(player[1])
            deaths = "{:03}".format(player[2])
            ratio = "{:3}".format(player[3])
            field_str += f"{name}\n⚔️:`{kills}` 💀:`{deaths}` K/D:`{ratio}`\n{'‾' * 24}\n"
    embed.add_field(name=map_str_name, value=field_str, inline=False)
    return embed 


def every_map_leaderboard_embed(map_data: dict):
    embed = Embed(title="Leaderboard", description=f"Top Players from all maps with a positive K/D", timestamp=datetime.datetime.now(), color=Color.blurple())
    for map_idx, map_name in enumerate(map_data.keys()):
        field_str = ""
        player_idx = 0
        map_str_name = f"**[{map_idx}] {map_name}**"
        for player in map_data[map_name]:
            name = "{:24}".format(f"{get_title_emoji(player_idx)} `{player[0]}` {get_title_emoji(player_idx)}")
            kills = "{:03}".format(player[1])
            deaths = "{:03}".format(player[2])
            ratio = "{:3}".format(player[3])
            field_str += f"{name}\n⚔️:`{kills}` 💀:`{deaths}` K/D:`{ratio}`\n{'‾' * 24}\n"
            player_idx += 1
        embed.add_field(name=map_str_name, value=field_str, inline=True)
    return embed