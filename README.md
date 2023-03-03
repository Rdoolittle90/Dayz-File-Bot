# Platinum Dayz Bot

The Platinum Dayz Bot is a Discord bot designed to provide various functionalities to Platinum Dayz server users and owners. The bot facilitates interactions with in-game assets and offers server owners simple tools to manage their servers.

## Dependencies

The bot uses the following dependencies:

- `aiomysql` - Asynchronous connection to the database
- `aioftp` - File transfer facilitation
- `nextcord>=2.4.0` - Discord API wrapper

Additional dependencies can be found in the `requirements.txt` file.

## Features

### User Features

- `register` - Registers the user to the bot.
- `profile` - Displays an embed with the user profile information.
- `atm` - Shows users their ATMs across all servers.
- `inventory` (not yet implemented) - Custom inventory system for Discord to allow users to have digital items to collect and trade in the Discord.
- `trade` (not yet implemented) - Intended to be the trade command for the inventory system.

### Admin Commands

The bot provides the following core admin commands:

- `set_announcement_channel` - Sets the bot's announcement channel to the given channel ID.
- `make_announcement` - Makes an announcement in the announcement channel.
- `bot_shutdown` - Kills the bot, requiring a manual reboot.
- `upload_trader_config` - Uploads trader config files to populate the database with trader items, prices, and other relevant information.

The bot also provides the following DayZ admin commands:

- `set_status` - Sets the status of the server to either offline, online, or restarting.
- `load_traderconfig` - Renders the TraderConfig.txt file for the selected map.
- `add_map` - Creates a new directory for the given map name.
- `remove_map` - Opens the map deletion modal.
- `get_key` - Looks up the passkey for the given map name.

## Getting Started

To use the Platinum Dayz Bot, users need to register their game account with the bot. The bot will also collect relevant server information automatically. The bot also requires certain permissions to function properly.

To access the admin commands, users need the appropriate server role assigned to them.

## Credits

The Platinum Dayz Bot was developed by InterfaceYourself.