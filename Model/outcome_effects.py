# Standard library imports  
from dataclasses import dataclass, field
from typing import Optional
from abc import ABC, abstractmethod
import enum

# Local application imports
from Model.player import Player
from Model.utils import Dice



class Effect(ABC):  
    @abstractmethod
    def modify_player(self, player: Player) -> None:
        ...


@dataclass
class RestoreHealth(Effect):
    amount: int
    def modify_player(self, player: Player) -> None:
        player.hp.restore(self.amount)


@dataclass
class LoseHealth(RestoreHealth):
    def modify_player(self, player: Player) -> None:
        player.hp.restore(-self.amount)


@dataclass
class ReceiveItem(Effect):
    item: str
    amount: int
    def modify_player(self, player: Player) -> None:
        player.add(self.item, self.amount)


@dataclass
class LoseItem(ReceiveItem):
    def modify_player(self, player: Player) -> None:
        player.remove(self.item, self.amount)


class OutcomeEffects(enum.Enum):
    LoseHealth = "Taken Damage"
    RestoreHealth = "Restore Health"
    ReceiveItem = "Receive Reward"
    LoseItem = "Lost Item"


OUTCOME_EFFECTS: dict[OutcomeEffects, type[Effect]] = {
    OutcomeEffects.LoseHealth: LoseHealth,
    OutcomeEffects.RestoreHealth: RestoreHealth,
    OutcomeEffects.ReceiveItem: ReceiveItem,
    OutcomeEffects.LoseItem: LoseItem}


@dataclass
class Outcome():
    result: str = field(repr=False)
    effect: Optional[Effect] = field(default=None, repr=False)

    def add_requirement(self, requirement) -> None:
        if not hasattr(requirement, "requirement"):
            self.requirement = [requirement]
        else:
            self.requirement.append(requirement)
    
    def modify_player(self, player: Player) -> None:
        if self.effect: self.effect.modify_player(player)

