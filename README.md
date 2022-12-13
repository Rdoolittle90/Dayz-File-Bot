# Dayz File Bot
Scope and Features still under heavy development

## Purpose
This bot is intended to be used as a Dayz server manager in bot file management and discord managment capacity


### Current Features
* Adds slash commands related to server status announcement
* Adds slash commands related to adding and removing maps from the manager
* Create `Types.xml` and `TraderConfig.txt` using MySQL database stored values
    - Limited to BotManagers per discord server.
    - Sends the rendered files to the discord user issuing the command
* Import `Types.xml` and/or `TraderConfig.txt` files via discord
    - Limited to Admins per discord server.
    - Stores the import file for future use
    - Import files are used to load the database with existing `Types.xml` or `TraderConfig.txt` files


### Expected Features
* Manager player ATM within discord
    - Requires **FTP** to connect to the required files to pull ATM
* Add user commands to allow for minigames within discord that affect ingame rewards
    - Raffle system
    - Simple Gambling minigames
* Add Ranking system for users based on time played in server
* Full multi-server support 