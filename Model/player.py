# Standard library imports  

# Local application imports
from Model.creature import Creature
from Model.stats import CapacityStat


class Player(Creature):
    pass

def create_player(name) -> Player:
    hp = CapacityStat(10, .2)
    mana = CapacityStat(0, 0)
    stamina = CapacityStat(10, .2)
    return Player(name, hp, mana, stamina)