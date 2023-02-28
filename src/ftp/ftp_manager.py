import datetime
import json
import os
import aioftp
import aiofiles
from os import getenv
from typing import Dict

# Maps the name of a map to a port number
port_by_name: Dict[str, int] = {
    "Chernarus": 21,
    "Takistan": 22,
    "Namalsk": 23,
    "TestServer": 24
}

class FTPConnect:
    """A class to manage connections to an FTP server and perform file transfers.

    Attributes:
        host (str): The host address of the FTP server.
        port (int): The port number to connect to on the FTP server.
        user (str): The username to use when authenticating with the FTP server.
        passwd (str): The password to use when authenticating with the FTP server.
        pool (aioftp.ConnectionPool): A connection pool to manage connections to the FTP server.
    """
    def __init__(self):
        """Initializes an FTPConnect object with default values for its attributes."""
        self.host: str = getenv("FTP_HOST")
        self.user: str = getenv("FTP_USER")
        self.passwd: str = getenv("FTP_PASSWORD")

    async def get_all_player_atm(self, map_name):
        async with aioftp.Client() as client:
            await client.connect(host=self.host, port=port_by_name[map_name])
            await client.login(user=self.user, password=self.passwd)
            print(f"Connecting to {self.host}:{port_by_name[map_name]} {map_name}")
            try:
                async for path, info in await client.list("/"):
                    if info["type"] == "file" and path.suffix == ".json":
                        async with aiofiles.open(path.name, mode="r") as f:
                            contents = await f.read()
                            data = json.loads(contents)
                            print(data)
            except aioftp.StatusCodeError as e:
                print(f"Error: {e.message}")
            finally:
                await client.quit()

    async def get_one_player_atm(self, map_name, SK64):
        async with aioftp.Client() as client:
            await client.connect(host=self.host, port=port_by_name[map_name])
            await client.login(user=self.user, password=self.passwd)
            try:
                path = f"{SK64}.json"
                if await client.exists(path):
                    async with aiofiles.open(path, mode="r") as f:
                        contents = await f.read()
                        data = json.loads(contents)
                        print(data)
            except aioftp.StatusCodeError as e:
                print(f"Error: {e.message}")
            finally:
                await client.quit()