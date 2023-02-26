import json
import asyncio
import aioftp
import aiofiles
from os import getenv

port_by_name = {
    "Chernarus": 21,
    "Takistan": 22,
    "Namalsk": 23,
    "TestServer": 24
}

class FTPConnect:
    def __init__(self):
        self.host = "135.148.136.106"
        self.port = ""
        self.user = "drifter"
        self.passwd = "waPreSPeHuF3"
        self.pool = None

    async def init_ftp(self, map_name):
        self.pool = await aioftp.Pool().make_connection(
            host= self.host,
            port= port_by_name[map_name],
            user= self.user,
            password= self.passwd,
            max_size= 4,
        )

    async def get_file(self, path, filename):
        async with self.pool.acquire() as conn:
            async with conn.client as client:
                async with client.download_stream(filename) as stream:
                    async with aiofiles.open(f"{path}/{filename}", "wb") as file:
                        async for chunk in stream.iter_by_block():
                            await file.write(chunk)

    async def update_atm(self, SK64, map_name, amount):
        path = f"_files/919677581824000070/maps/{map_name}/atms/{SK64}.json"

        with open(path, "r") as fin:
            player_ATM = json.load(fin)

        player_ATM["currentMoney"] += amount

        with open(path, "w") as fout:
            json.dump(player_ATM, fout, indent=4)

        async with self.pool.acquire() as conn:
            async with conn.client as client:
                await client.upload(f"{SK64}.json", f"{path}/{SK64}.json")

    async def get_all_player_atm(self, serverID):
        async with self.pool.acquire() as conn:
            async with conn.client as client:
                await client.change_directory("profiles/LBmaster/Data/LBBanking/Players")
                files = await client.list()
                for file in files:
                    if file.name.endswith(".json"):
                        await self.get_file(f"_files/maps/{self.map}/atms/", file.name)
                await client.change_directory("../../../../../")

    async def get_one_player_atm(self, SK64, serverID=919677581824000070):
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