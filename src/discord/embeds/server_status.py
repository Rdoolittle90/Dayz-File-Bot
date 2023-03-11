


import datetime

import nextcord

from src.discord.bot import DiscordBot


def server_status_embed(bot: DiscordBot):
    utc_now = datetime.datetime.utcnow()
    now = datetime.datetime.now()

    time_diff = utc_now - bot.cftools.utc_then
    if time_diff >= datetime.timedelta(seconds=30) or bot.cftools.server_info[0] == {}:
        bot.cftools.utc_then = utc_now
        for idx, server_map in enumerate(bot.cftools.map_info.keys()):
            server_id = bot.cftools.map_info[server_map]["map_id"]
            response = bot.cftools.make_authenticated_request("GET", f"https://data.cftools.cloud/v1/gameserver/{server_id}")
            data = response.json()
            name = data[server_id]['name'].split(" ")[1].title()
            bot.cftools.server_info[idx]["name"] = name
            bot.cftools.server_info[idx]["status"] = "Online" if data[server_id]['online'] else "Offline"
            bot.cftools.server_info[idx]["players"] = data[server_id]['status']['players']
            bot.cftools.server_info[idx]["slots"] = data[server_id]['status']['slots']


    server_status_list = [
        bot.cftools.server_info[0]["status"], 
        bot.cftools.server_info[1]["status"], 
        bot.cftools.server_info[2]["status"]
    ]
    
    color, status_emoji = format_status(server_status_list)
    # Create a new embed
    embed = nextcord.Embed(title="Platinum Server Status", color=color, timestamp=now)

    # Add fields to the embed
    for idx in range(0, 3):
        name = bot.cftools.server_info[idx]["name"]
        status = bot.cftools.server_info[idx]["status"]
        players = bot.cftools.server_info[idx]["players"]
        slots = bot.cftools.server_info[idx]["slots"]

        embed.add_field(
            name=f'[#{idx+1}] {name}', 
            value=f'{status_emoji}: `{status}`\nPlayers: `{players}/{slots}`', 
            inline=True
            )
        
    return embed
        

def format_status(server_status_list: list[bool]) -> tuple[nextcord.Color, str]:
    """
    Given a list of 3 booleans representing server statuses, returns a tuple containing a color and a status emoji.

    Args:
    - server_status_list (list[bool]): A list of 3 booleans representing server statuses, where True means the server is online and False means it is offline.

    Returns:
    - A tuple containing a `nextcord.Color` object and a string representing a status emoji.
    """
    if all(server_status_list):
        # If all servers are online, set the color to green and the emoji to a green circle.
        color = nextcord.Color.green()
        status_emoji = "🟢"
    elif not any(server_status_list):
        # If all servers are offline, set the color to red and the emoji to a red circle.
        color = nextcord.Color.red()
        status_emoji = "🔴"
    else:
        # Otherwise, set the color to orange and the emoji to an orange circle.
        color = nextcord.Color.orange()
        status_emoji = "🟠"

    # Return a tuple containing the color and status emoji.
    return color, status_emoji