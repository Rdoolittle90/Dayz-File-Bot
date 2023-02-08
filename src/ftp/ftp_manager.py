from ftplib import FTP
import json
from os import getenv


port_by_name = {
    "Chernarus": 21,
    "Takistan": 22,
    "Namalsk": 23,
    "TestServer": 24
}


class FTPConnect():
    def __init__(self, map_name):
        self.map = map_name
        self.host = "135.148.136.106"
        self.port = port_by_name[map_name]
        self.user = "drifter"
        self.passwd = "waPreSPeHuF3"

        self.ftp = FTP()
        self.ftp.set_debuglevel(0)


    def connect(self):
        self.ftp.connect(host=self.host, port=self.port)
        self.ftp.login(user=self.user, passwd=self.passwd)


    def getFile(self, path, File_name):
        with open(f"{path}/{File_name}", "wb") as ftb_in:
            self.ftp.retrbinary(f"RETR {File_name}", ftb_in.write, 1024)


    def UpdateATM(self, SK64, map_name, amount):
        path = f"_files/919677581824000070/maps/{map_name}/atms/{SK64}.json"

        with open(path, "r") as fin:
            player_ATM = json.load(fin)

        player_ATM["currentMoney"] += amount

        with open(path, "w") as fout:
            json.dump(player_ATM, fout, indent=4)

        self.ftp.cwd("profiles/LBmaster/Data/LBBanking/Players")
        with open(path, "rb") as ftb_out:
            self.ftp.storbinary(f"STOR {SK64}.json", ftb_out)
        self.ftp.cwd("../../../../../")



    def getAllPlayerATM(self, serverID):
        self.ftp.cwd("profiles/LBmaster/Data/LBBanking/Players")
        files = self.ftp.nlst()
        for file in files:
            if file.endswith(".json"):
                self.getFile(f"_files/{serverID}/maps/{self.map}/atms/", file)
        self.ftp.cwd("../../../../../")



    def getOnePlayerATM(self, SK64, serverID=919677581824000070):
        self.ftp.cwd("profiles/LBmaster/Data/LBBanking/Players")
        files = self.ftp.nlst()
        if f"{SK64}.json" in files:
            self.getFile(f"_files/{serverID}/maps/{self.map}/atms/", f"{SK64}.json")
        self.ftp.cwd("../../../../../")

    def getOmegaConfig(self):
        self.getFile(f"_files/support/", "omega.cfg")

    def quit(self):
        self.ftp.quit()



if __name__ == "__main__":
    ftp = FTPConnect("Namalsk", 
        getenv("FTP_IP"), int(getenv("FTP_PORT_1")), 
        getenv("FTP_USER"), getenv("FTP_PASSWORD")
    ) #FIXME

    ftp.getOmegaConfig()
