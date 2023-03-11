import json


def update_money(player_atm: dict, player_path: str, amount: int = 0) -> int|str|None:
    if amount < 0:
        if player_atm["currentMoney"] < abs(amount):
            return "You dont have enough money."
    player_atm["currentMoney"] = player_atm["currentMoney"] + amount
    with open(player_path, 'w') as atm_out:
        json.dump(player_atm, atm_out, indent=4)

    return int(player_atm["currentMoney"])