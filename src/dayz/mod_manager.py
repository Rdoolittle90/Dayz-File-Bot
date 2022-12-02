import json
from ftp.ftp_manager import FTPConnect
from src.sql.sql_manager import DBConnect


def update_mod_list(map_name):
    ftp = FTPConnect("Namalsk", ) #FIXME
    ftp.getOmegaConfig()
    
    with open(f"_files/support/{map_name}/omega.cfg", "r") as fin:
        mod_list = json.load(fin)

    for mod in mod_list["mods"]:
        sql = DBConnect()
        sql.insert_into_server_mods(map_name, mod)
        sql.commit()
    sql.close()