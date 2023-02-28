import os
from typing import Dict
from twisted.internet import defer, reactor, protocol
from twisted.python.filepath import FilePath
from twisted.protocols.ftp import FTPClient, FTPFileListProtocol

ftp_port_by_name: Dict[str, int] = {"Chernarus": 21, "Takistan": 22, "Namalsk": 23, "TestServer": 24}

class FTPConnect:
    def __init__(self):
        self.host: str = os.getenv("FTP_HOST")
        self.user: str = os.getenv("FTP_USER")
        self.passwd: str = os.getenv("FTP_PASSWORD")

    @defer.inlineCallbacks
    def download_all_atm_json_files(self, map_name: str):
        print(f"Attempting to connect to {map_name}")
        client = yield protocol.ClientCreator(reactor, FTPClient).connectTCP(self.host, ftp_port_by_name[map_name])
        print(f"Connected to {map_name}")
        yield client.login(self.user, self.passwd)
        print(f"Logged in to {map_name}")
        yield client.cwd("profiles/LBmaster/Data/LBBanking/Players")
        print(f"Changed working directory to 'profiles/LBmaster/Data/LBBanking/Players' on {map_name}")
        file_list_protocol = FTPFileListProtocol()
        yield client.list(".", file_list_protocol)
        files = file_list_protocol.files
        print(f"Listed files on {map_name}")
        for filename, attrs in files:
            if not filename.endswith(".json"):
                continue
            print(f"Downloading {filename} from {map_name}")
            local_filepath = FilePath(f"_files/maps/atms/{filename}")
            with open(local_filepath.path, "wb") as f:
                yield client.retrieveFile(filename, f)
            print(f"Downloaded {filename} from {map_name}")
        client.quit()
        print(f"Disconnected from {map_name}")