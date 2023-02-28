import os
from typing import Dict

from twisted.internet import defer, reactor, protocol
from twisted.python.filepath import FilePath
from twisted.protocols.ftp import FTPClient, FTPFileListProtocol


# Maps the name of a map to an FTP path
ftp_port_by_name: Dict[str, int] = {
    "Chernarus": 21,
    "Takistan": 22,
    "Namalsk": 23,
    "TestServer": 24
}

class FTPConnect:
    """A class to manage connections to an FTP server and perform file transfers.

    Attributes:
        host (str): The host address of the FTP server.
        user (str): The username to use when authenticating with the FTP server.
        passwd (str): The password to use when authenticating with the FTP server.
    """

    def __init__(self):
        """Initializes an FTPConnect object with default values for its attributes."""
        self.host: str = os.getenv("FTP_HOST")
        self.user: str = os.getenv("FTP_USER")
        self.passwd: str = os.getenv("FTP_PASSWORD")

    @defer.inlineCallbacks
    def download_all_atm_json_files(self, map_name: str):
        """
        Downloads all JSON files in the /profiles/LBmaster/Data/LBBanking/Players directory on the FTP server
        to the local _files/maps/atms directory.

        Args:
            map_name (str): The name of the map to download the JSON files for.
        """
        # Connect to the FTP server
        client = yield protocol.ClientCreator(reactor, FTPClient).connectTCP(self.host, ftp_port_by_name[map_name])
        yield client.login(self.user, self.passwd)
        print(f"Connected to {map_name}")
        # Change to the correct directory
        yield client.cwd("profiles/LBmaster/Data/LBBanking/Players")

        # List all files in the directory
        file_list_protocol = FTPFileListProtocol()
        yield client.list(".", file_list_protocol)
        files = file_list_protocol.files
        print(files)
        # Download each JSON file to the _files/maps/atms directory
        for filename, attrs in files:
            if not filename.endswith(".json"):
                continue

            local_filepath = FilePath(f"_files/maps/atms/{filename}")
            with open(local_filepath.path, "wb") as f:
                yield client.retrieveFile(filename, f)

        client.quit()