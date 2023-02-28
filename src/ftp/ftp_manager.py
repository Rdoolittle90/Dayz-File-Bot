import os
from typing import Dict
from twisted.internet import defer, reactor, protocol
from twisted.python.filepath import FilePath
from twisted.protocols.ftp import FTPClient, FTPFileListProtocol
from twisted.logger import Logger, LogLevel, globalLogPublisher

ftp_port_by_name: Dict[str, int] = {"Chernarus": 21, "Takistan": 22, "Namalsk": 23, "TestServer": 24}
logger = Logger(namespace="ftpconnect")

class FTPConnect:
    def __init__(self):
        self.host: str = os.getenv("FTP_HOST")
        self.user: str = os.getenv("FTP_USER")
        self.passwd: str = os.getenv("FTP_PASSWORD")
        globalLogPublisher.addObserver(logger)

    @defer.inlineCallbacks
    def download_all_atm_json_files(self, map_name: str):
        logger.info(f"Attempting to connect to {map_name}")
        client = yield protocol.ClientCreator(reactor, FTPClient).connectTCP(self.host, ftp_port_by_name[map_name])
        logger.info(f"Connected to {map_name}")
        yield client.login(self.user, self.passwd)
        logger.info(f"Logged in to {map_name}")
        yield client.cwd("profiles/LBmaster/Data/LBBanking/Players")
        logger.info(f"Changed working directory to 'profiles/LBmaster/Data/LBBanking/Players' on {map_name}")
        file_list_protocol = FTPFileListProtocol()
        yield client.list(".", file_list_protocol)
        files = file_list_protocol.files
        logger.info(f"Listed files on {map_name}")
        for filename, attrs in files:
            if not filename.endswith(".json"):
                continue
            logger.info(f"Downloading {filename} from {map_name}")
            local_filepath = FilePath(f"_files/maps/atms/{filename}")
            with open(local_filepath.path, "wb") as f:
                yield client.retrieveFile(filename, f)
            logger.info(f"Downloaded {filename} from {map_name}")
        client.quit()
        logger.info(f"Disconnected from {map_name}")