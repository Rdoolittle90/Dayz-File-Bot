import random


def price_assist_by_rarity(rarity: int):
    if rarity == 0:
        value = random.randint(500, 5000)
        value -= value % 100
    elif rarity == 1:
        value = random.randint(3500, 10000)
        value -= value % 100
    elif rarity == 2:
        value = random.randint(15000, 35000)
        value -= value % 100
    elif rarity == 3:
        value = random.randint(70000, 100000)
        value -= value % 100
    else:
        value = 150000

    return value


    
def get_nominality(value):
    pass