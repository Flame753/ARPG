# Standard library imports 
from dataclasses import dataclass, field, fields, astuple
from typing import Optional, Protocol
import random
import enum

# Local application imports
from Model.player import Player
from View.ui import UI
import Model.utils as utils
from Model.economy import Currency


class InvalidInput(Exception):
    """Exception raised for an Invalid Input was entered."""
    
    def __init__(self, message="Invalid Input was entered!"):
        self.message = message
        super().__init__(self.message)


class Decision(enum.Enum):
    A = enum.auto()
    B = enum.auto()
    C = enum.auto()
    D = enum.auto()

def decision_gen():
    for d in Decision:
        yield d 


class OutcomeEffects(enum.Enum):
    TakenDamage = "Taken Damage"
    RestoreHealth = "Restore Health"
    ReceiveReward = "Receive Reward"
    LostItem = "Lost Item"


class Effect(Protocol):  
    def modify_player(self, player: Player) -> None:
        ...


@dataclass
class TakenDamage(Effect):
    amount: int
    def modify_player(self, player: Player) -> None:
        player.hp -= self.amount


@dataclass
class RestoreHealth(TakenDamage):
    def modify_player(self, player: Player) -> None:
        player.hp += self.amount
        if player.hp > player.max_hp:
            player.hp = player.max_hp


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


OUTCOME_EFFECTS: dict[OutcomeEffects, type[Effect]] = {
    OutcomeEffects.TakenDamage: TakenDamage,
    OutcomeEffects.RestoreHealth: RestoreHealth,
    OutcomeEffects.ReceiveReward: ReceiveReward,
    OutcomeEffects.LostItem: LostItem}


@dataclass
class Outcome():
    text: str = field(repr=False)
    effect: Optional[Effect] = field(default=None, repr=False)

    def add_requirement(self, requirement) -> None:
        if not hasattr(requirement, "requirement"):
            self.requirement = [requirement]
        else:
            self.requirement.append(requirement)
    
    def modify_player(self, player: Player) -> None:
        if self.effect: self.effect.modify_player(player)


@dataclass
class Event:
    into_text: str = ""
    pre_outcome: list = field(default_factory=list)
    post_outcome: list = field(default_factory=list)

    def set_into_text(self, text: str):
        self.into_text = text

    def add_outcome(self, pre_outcome: Outcome, post_outcome: Outcome):
        self.pre_outcome.append(pre_outcome)
        self.post_outcome.append(post_outcome)
    

def BrokenCart():
    e = Event()
    into_text = "You were walking down a path and see a carriage with a broken wheel on the side of the road. "
    option1 = Outcome(text="Do you stop and help repaire the carriage? ")
    option2 = Outcome(text="Or, continue on your journey. ")
    outcome1 = Outcome(text="After spending a few hours fixing the carriage. " \
                            "A old man steps out of the carriage and thanks you for fixing his carriage. " \
                            "He gives you 2 small gold coins. ",
                        effect=ReceiveReward(item=Currency.Gold, amount=2))
    outcome2 = Outcome(text="You mind your own business and pass the traveler. Nothing happens. ")

    e.set_into_text(into_text)
    e.add_outcome(option1, outcome1)
    e.add_outcome(option2, outcome2)
    return e

def BridHunt():
    e = Event()
    into_text = "You see a flock of bird flying over head. " \
                "It seem like a great change to get a easy meal. "
    option1 = Outcome(text="Shot a it down.")
    option2 = Outcome(text="Let it fly pass you. ")
    outcome1 = Outcome(text="After taking aim and releasing your arrow. " \
                            "It hits your mark and you made a great meal out of your hunt. " \
                            "Nothing else happened that day. ")
    outcome2 = Outcome(text="You let the flock of bird fly pass you. " \
                            "Nothing else eventful happened. ")

    e.set_into_text(into_text)
    e.add_outcome(option1, outcome1)
    e.add_outcome(option2, outcome2)
    return e


def breakingtest():
    e = Event()
    into_text = "Testing!"
    option1 = Outcome(text="option1")
    option2 = Outcome(text="option2")
    option3 = Outcome(text="option3")
    option4 = Outcome(text="option4")
    outcome1 = Outcome(text="outcome1")
    outcome2 = Outcome(text="outcome2")
    outcome3 = Outcome(text="outcome3")
    outcome4 = Outcome(text="outcome4")

    e.set_into_text(into_text)
    e.add_outcome(option1, outcome1)
    e.add_outcome(option2, outcome2)
    e.add_outcome(option3, outcome3)
    e.add_outcome(option4, outcome4)
    return e


class RoadEvents(enum.Enum):
    BrokenCart = BrokenCart()
    BridHunt = BridHunt()
    bad = breakingtest()
