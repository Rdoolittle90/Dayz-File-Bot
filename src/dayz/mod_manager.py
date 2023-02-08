from src.ftp.ftp_manager import FTPConnect
from src.sql.sql_manager import DBConnect


def update_player_atm(map_name:str, DUID:int, amount:int, serverID:int=919677581824000070):
    ftp = FTPConnect("TestServer", "135.148.136.106", "ryan", "Platinum1234") #FIXME
    ftp.connect()

    sql = DBConnect()
    sql.select_SK64_from_registration(DUID)
    SK64 = sql.c.fetchone()
    if SK64:
        SK64 = int(SK64[0])
        ftp.getOnePlayerATM(serverID, SK64)
        ftp.UpdateATM(serverID, SK64, map_name, amount)
        ftp.quit()
        return 1

    # SK64 not found
    print("ID not found")
    ftp.quit()
    return 0
