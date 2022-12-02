from ftplib import FTP



class FTPConnect():
    def __init__(self, map_name, host, port, user, passwd):
        self.map = map_name

        self.ftp = FTP()
        self.ftp.connect(host=host, port=port)
        self.ftp.login(user=user, passwd=passwd)

    def getFile(self, path, File_name):
        with open(f"{path}/{self.map}/{File_name}", "wb") as ftb_in:
            self.ftp.retrbinary(f"RETR {File_name}", ftb_in.write, 1024)


    def setFile(self, File_name):
        with open(File_name, "rb") as ftb_out:
            self.ftp.storbinary(f"STOR {File_name}", ftb_out)

    def getAllPlayerATM(self):
        self.ftp.cwd("/profiles/DC_Banking/PlayerDatabase")
        files = self.ftp.nlst()
        for file in files:
            self.getFile(f"_files/atms", file)
        self.ftp.cwd("../../../")

    def getOmegaConfig(self):
        self.getFile(f"_files/support/", "omega.cfg")

    def quit(self):
        self.ftp.quit()



if __name__ == "__main__":
    ftp = FTPConnect() #FIXME

    ftp.getOmegaConfig()
