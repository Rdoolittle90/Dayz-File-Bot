from disnake import DMChannel
import requests
from disnake.message import Message
from disnake.ext.commands import Bot
from src.discord.guild_manager import initial_cha_setup, initial_server_setup

from src.file_manager import create_new_server_dir, initial_dir_setup


class MyClient(Bot):
    async def on_ready(self):
        initial_dir_setup()
        print("Connected to:")
        for guild in self.guilds:
            print('\t', guild.name)
            await initial_cha_setup(guild)
            await initial_server_setup(guild)
            create_new_server_dir(guild.id)
        print(f'Logged on as: {self.user}')




    async def on_message(self, message: Message):
        if isinstance(message.channel, DMChannel):
            return
        if message.channel.name != "drifter-imports":
            return
        if len(message.content) == 0:
            return

        map_name = message.content.split(" ")[1]
        attachments = message.attachments
        await message.delete()
        if len(attachments) > 0:
            for file in attachments:
                response = requests.get(file.url)
                try:
                    if file.filename.endswith(".txt"):
                        with open(f"_files/{message.guild.id}/maps/{map_name}/inputs/{file.filename}", "w") as text_out:
                            text_out.write(response.content.decode('utf-8'))

                    elif file.filename.endswith(".xml"):
                        with open(f"_files/{message.guild.id}/maps/{map_name}/inputs/{file.filename}", "wb") as xml_out:
                            xml_out.write(response.content)

                except FileNotFoundError:
                    print("something went wrong")
                    print(f"_files/{message.guild.id}/maps/{map_name}/inputs/{file.filename}")
                    print("Not found")