import json
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
        self.port: int = ""
        self.user: str = getenv("FTP_USER")
        self.passwd: str = getenv("FTP_PASSWORD")
        self.pool: aioftp.ConnectionPool = None

    async def init_ftp(self, map_name: str) -> None:
        """Initializes the connection pool for the FTP server.

        Args:
            map_name (str): The name of the map to connect to on the FTP server.

        Raises:
            aioftp.errors.ClientError: If the connection pool could not be created.
        """
        self.pool = await aioftp.Pool().make_connection(
            host=self.host,
            port=port_by_name[map_name],
            user=self.user,
            password=self.passwd,
            max_size=4,
        )

    async def get_file(self, path: str, filename: str) -> None:
        """Downloads a file from the FTP server.

        Args:
            path (str): The path to download the file to.
            filename (str): The name of the file to download.

        Raises:
            aioftp.errors.ClientError: If the file could not be downloaded.
        """
        async with self.pool.acquire() as conn:
            async with conn.client as client:
                async with client.download_stream(filename) as stream:
                    async with aiofiles.open(f"{path}/{filename}", "wb") as file:
                        async for chunk in stream.iter_by_block():
                            await file.write(chunk)

    async def update_atm(self, SK64, map_name, amount):
        """Updates the balance of an ATM belonging to a player.

        Args:
            SK64 (str): The unique identifier of the player whose ATM should be updated.
            map_name (str): The name of the map that the player is on.
            amount (int): The amount of money to add to the player's ATM.

        Raises:
            FileNotFoundError: If the player's ATM file could not be found.
            json.JSONDecodeError: If the player's ATM file could not be decoded.
            aioftp.errors.ClientError: If the player's ATM file could not be uploaded.
        """
        path = f"_files/maps/{map_name}/atms/{SK64}.json"

        with open(path, "r") as fin:
            player_ATM = json.load(fin)

        player_ATM["currentMoney"] += amount

        with open(path, "w") as fout:
            json.dump(player_ATM, fout, indent=4)

        async with self.pool.acquire() as conn:
            async with conn.client as client:
                await client.upload(f"{SK64}.json", f"{path}/{SK64}.json")

    async def get_all_player_atm(self):
        async with self.pool.acquire() as conn:
            async with conn.client as client:
                await client.change_directory("profiles/LBmaster/Data/LBBanking/Players")
                files = await client.list()
                for file in files:
                    if file.name.endswith(".json"):
                        await self.get_file(f"_files/maps/{self.map}/atms/", file.name)
                await client.change_directory("../../../../../")

    async def get_one_player_atm(self, SK64):
        async with self.pool.acquire() as conn:
            async with conn.client as client:
                await client.change_directory("profiles/LBmaster/Data/LBBanking/Players")
                files = await client.list()
                if f"{SK64}.json" in [file.name for file in files]:
                    await self.get_file(f"_files/maps/{self.map}/atms/", f"{SK64}.json")
                await client.change_directory("../../../../../")

    async def get_omega_config(self):
        async with self.pool.acquire() as conn:
            async with conn.client as client:
                await self.get_file(f"_files/support/", "omega.cfg")

    async def quit(self):
        await self.pool.close()