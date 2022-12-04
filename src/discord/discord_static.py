from disnake.ext.commands import Bot

from src.file_manager import create_new_server_dir


class MyClient(Bot):
    async def on_ready(self):
        print("Connected to:")
        for guild in self.guilds:
            create_new_server_dir(guild.id)
            print('\t', guild.name)
        print(f'Logged on as: {self.user}')
