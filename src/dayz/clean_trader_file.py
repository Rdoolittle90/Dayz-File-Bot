

def open_config(guild_id, map_name):
    with open(f"_files/{guild_id}/maps/{map_name}/inputs/TraderConfig.txt", "r") as fin:
        lines = fin.readlines()
    return lines


def parse_config(lines) -> list[str]:
    items = []
    for line in lines[18:]:
        line: str
        if line.startswith("<Trader> ") or line.startswith("<CurrencyName>") or line.startswith("<FileEnd>"):
            trader = line.strip("<Trader> ").replace("\n", "").replace("\t", "").split("//")[0].strip()
        elif line.startswith("\t<Category> ") or line.startswith("\t<Currency>"):
            category = line.strip("\t<Category> ").replace("\n", "").replace("\t", "").split("//")[0].strip()
        elif line.replace("\t", "").replace(" ", "").startswith("/"):
            continue
        else:
            line = line.replace("\t", "")
            line = line.replace("\n", "")
            line = line.replace(" ", "")

            line = line.split(",")
            if len(line) == 1:
                continue
            try:
                comment_index = line[3].rfind("//")
                if comment_index >= 0:
                    line[3] = line[3][:comment_index]
            except IndexError as err:
                print("no comment")
                
            items.append([trader, category, line[0], line[1], int(line[2]), int(line[3])])
    return items