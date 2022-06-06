# Standard library imports 
from dataclasses import dataclass
import enum

# Local application imports
from Model.stats import CapacityStat

@dataclass
class Creature():
    name: str
    hp: CapacityStat
    mana: CapacityStat
    stamina: CapacityStat
    
    def is_alive(self) -> bool:
        return not self.hp.is_empty()

    def have_mana(self) -> bool:
        return not self.mana.is_empty()
    
    def have_stamina(self) -> bool:
        return not self.stamina.is_empty()


class Enemy(enum.Enum):
    GiantSpider = Creature("Giant Spider", hp=CapacityStat(10, .2), mana=CapacityStat(0, 0), stamina=CapacityStat(30, .5))
    Ogre = Creature("Ogre", hp=CapacityStat(30, .2), mana=CapacityStat(0, 0), stamina=CapacityStat(30, .1))
    BatColony = Creature("Bat of Colony",hp=CapacityStat(100, .2), mana=CapacityStat(0, 0), stamina=CapacityStat(15, .5))
    RockMonster = Creature("Rock Monster", hp=CapacityStat(80, .2), mana=CapacityStat(20, .2), stamina=CapacityStat(4, .1))


# class Creature():
#     def __init__(self, name: str, max_hp: int, damage: int) -> None:
#         self.name = name
#         self.hp = max_hp
#         self.max_hp = max_hp
#         self.damage = damage

#     def is_alive(self) -> bool:
#         return self.hp > 0


# class Enemy(enum.Enum):
#     GiantSpider = Creature("Giant Spider", max_hp=10, damage=2)
#     Ogre = Creature("Ogre", max_hp=30, damage=10)
#     BatColony = Creature("Bat of Colony", max_hp=100, damage=4)
#     RockMonster = Creature("Rock Monster", max_hp=80, damage=15)
