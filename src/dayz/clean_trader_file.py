def open_config(guild_id, map_name):
    with open(f"_files/{guild_id}/maps/{map_name}/inputs/TraderConfig.txt", "r") as fin:
        lines = fin.readlines()
    return lines


def prep_category_name(line:str):
    start = line.rfind(">")
    end = line.rfind("//")
    category = line[start+1:end].strip()
    return category


def parse_config(lines: list[str]) -> list[str]:
    items = []
    for line in lines[18:]:
        if line.startswith("<Trader>") or line.startswith("<CurrencyName>") or line.startswith("<FileEnd>"):
            trader = prep_category_name(line)

        elif line.startswith("\t<Category>") or line.startswith("\t<Currency>"):
            category = prep_category_name(line)

        elif line.replace("\t", "").replace(" ", "").startswith("/"):
            continue

        else:
            line = line.replace("\t", "")
            line = line.replace("\n", "")
            line = line.replace(" ", "")

            line = line.split(",")
            if len(line) < 4:
                continue

            comment_index = line[3].rfind("//")
            if comment_index >= 0:
                line[3] = line[3][:comment_index]

            items.append([trader, category, line[0], line[1], int(line[2]), int(line[3])])
    return items