# Standard library imports 
from dataclasses import dataclass, field
import enum

# Local application imports
from Model.stats import CapacityStat
from Model.utils import Container
from Model.stats import Stats, PrimaryStat
from Model.experience import Level, Algorithms


@dataclass
class Creature():
    name: str
    level: Level = field(repr=False, init=False)
    stats: Stats = field(default_factory=Stats, repr=False, init=False)
    inventory: Container = field(default_factory=Container, repr=False, init=False)

    def __post_init__(self):
        self.level = Level(Algorithms.Creature.value)
    
    def is_alive(self) -> bool:
        return not self.stats.primary.get(PrimaryStat.Vigor).is_empty()

    def have_enough_mana(self) -> bool:
        return self.stats.primary.get(PrimaryStat.Arcane).have_enough()
    
    def have_enough_stamina(self) -> bool:
        return self.stats.primary.get(PrimaryStat.Endurance).have_enough()


# @dataclass
# class Creature():
#     name: str
    
#     hp: CapacityStat
#     mana: CapacityStat
#     stamina: CapacityStat
#     inventory: Container = field(default_factory=Container, repr=False, init=False)
    
#     def is_alive(self) -> bool:
#         return not self.hp.is_empty()

#     def have_mana(self) -> bool:
#         return not self.mana.is_empty()
    
#     def have_stamina(self) -> bool:
#         return not self.stamina.is_empty()



def GiantSpider():
    return Creature("Giant Spider", hp=CapacityStat(10, .2), mana=CapacityStat(0, 0), stamina=CapacityStat(30, .5))

def Ogre():
    return Creature("Ogre", hp=CapacityStat(30, .2), mana=CapacityStat(0, 0), stamina=CapacityStat(30, .1))

def BatColony():
    return Creature("Bat of Colony",hp=CapacityStat(100, .2), mana=CapacityStat(0, 0), stamina=CapacityStat(15, .5))

def RockMonster():
    return Creature("Rock Monster", hp=CapacityStat(80, .2), mana=CapacityStat(20, .2), stamina=CapacityStat(4, .1))


class Enemy(enum.Enum):
    GiantSpider = GiantSpider
    Ogre = Ogre
    BatColony = BatColony
    RockMonster = RockMonster