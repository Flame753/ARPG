# Standard library imports 
from dataclasses import dataclass, field
import enum


# Local application imports
from Model.experience import Level


class CoreStat(enum.Enum):
    Con = "Constitution"
    Str = "Strenght"
    Dex = "Dexterity"
    Int = "Intelligence"
    Wis = "Wisdom"
    Cha = "Charisma"


class PrimaryStat(enum.Enum):
    Vigor = "Health"
    Endurance = "Stamina"
    Arcane = "Magic"


@dataclass
class BaseStat:
    primary_core_stat: Level
    secondary_core_stat: Level


@dataclass
class CapacityStat(BaseStat):
    # regen_speed: float
    
    def __post_init__(self):
        self.current_value: int = self.capacity
        self._capacity: int = self.capacity

        # if self.regen_speed < 0 or self.regen_speed > 1:
        #     raise ValueError("Regeneration Speed must be a value between 0 and 1.")

    @property
    def capacity(self) -> int:
        primary = self.primary_core_stat.get_level()
        secondary = self.secondary_core_stat.get_level()//2
        base = 10
        return primary + secondary + base
    
    def is_empty(self) -> bool:
        return self.current_value == 0

    def have_enough(self, num: int) -> bool:
        return num <= self.current_value
    
    # @property
    # def regeneration_amount(self) -> int:
    #     return round(self.regen_speed * self.capacity)

    def restore(self, amount: int=0):
        if amount < 0: raise TypeError("Negative number is not acceptable!")
        self.current_value = min(self.capacity, self.current_value + amount) # Can't go over the capacity
    
    def loss(self, amount: int=0) -> bool:
        if amount < 0: raise TypeError("Negative number is not acceptable!")
        self.current_value = max(0, self.current_value - amount) # Can't go under Zero

    def update(self):
        capacity_change = self.capacity - self._capacity
        self.current_value += capacity_change
        self._capacity = self.capacity



@dataclass
class DefenceStat(BaseStat):
    physical_reduction: float
    magic_reduction: float
    dogde: float


@dataclass
class Stats:

    def __init__(self) -> None:
        self.points: int = 0

        self.core = {stat: {"level":Level(), "xp_bonus": 0} for stat in CoreStat}

        self.primary = {PrimaryStat.Vigor: CapacityStat(primary_core_stat=self.core.get(CoreStat.Con).get("level"),
                                                        secondary_core_stat=self.core.get(CoreStat.Str).get("level")),
                        PrimaryStat.Endurance: CapacityStat(primary_core_stat=self.core.get(CoreStat.Con).get("level"),
                                                        secondary_core_stat=self.core.get(CoreStat.Dex).get("level")),
                        PrimaryStat.Arcane: CapacityStat(primary_core_stat=self.core.get(CoreStat.Wis).get("level"),
                                                        secondary_core_stat=self.core.get(CoreStat.Int).get("level"))}
    
    def get_core_stat(self, stat: CoreStat):
        core_stat = self.core.get(stat)
        if not core_stat: raise KeyError(f"<{stat}> Isn't a vaild Core Stats!")
        return core_stat
    
    def apply_points(self, stat: CoreStat, amount: int):
        if amount < 0: raise TypeError("Negative number is not acceptable!")
        if amount > self.points: return
        core_stat = self.get_core_stat(stat)
        bonus = core_stat.get("xp_bonus")
        core_stat.update({"xp_bonus": bonus + amount})
        self.points -= amount

    
    def apply_xp(self, stat: CoreStat, amount: int):
        if amount < 0: raise TypeError("Negative number is not acceptable!")
        core_stat = self.get_core_stat(stat)
        bouns = core_stat.get("xp_bonus")
        core_stat.get("level").add_xp(amount + bouns)

    def get_level(self, stat: CoreStat) -> int:
        return self.get_core_stat(stat).get("level").get_level()

    def update(self):
        for stat in PrimaryStat:
            self.primary.get(stat).update()