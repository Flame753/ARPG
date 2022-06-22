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
class TakenDamage(Effect):
    amount: int
    def modify_player(self, player: Player) -> None:
        player.hp.restore(-self.amount)
        print("--------> Test print: (in outcome_effect module) ", player.hp.current )


@dataclass
class RestoreHealth(TakenDamage):
    def modify_player(self, player: Player) -> None:
        player.hp.restore(self.amount)


@dataclass
class ReceiveReward(Effect):
    item: str
    amount: int
    def modify_player(self, player: Player) -> None:
        player.add(self.item, self.amount)


@dataclass
class LostItem(ReceiveReward):
    def modify_player(self, player: Player) -> None:
        player.remove(self.item, self.amount)


class OutcomeEffects(enum.Enum):
    TakenDamage = "Taken Damage"
    RestoreHealth = "Restore Health"
    ReceiveReward = "Receive Reward"
    LostItem = "Lost Item"


OUTCOME_EFFECTS: dict[OutcomeEffects, type[Effect]] = {
    OutcomeEffects.TakenDamage: TakenDamage,
    OutcomeEffects.RestoreHealth: RestoreHealth,
    OutcomeEffects.ReceiveReward: ReceiveReward,
    OutcomeEffects.LostItem: LostItem}


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

