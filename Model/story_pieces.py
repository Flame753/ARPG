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


@dataclass
class RotatingDecision:
    def __init__(self) -> None:
        self.rotating_decision = iter(Decision)

    def next_decision(self) -> Decision:
        return next(self.rotating_decision)


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
        player.add_item(self.item, self.amount)


@dataclass
class LostItem(ReceiveReward):
    def modify_player(self, player: Player) -> None:
        player.remove_item(self.item, self.amount)


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

class RoadEvents(enum.Enum):
    BrokenCart = BrokenCart()
    BridHunt = BridHunt()


# @dataclass
# class Event:
#     def __init__(self, name: str, ui: UI, player: Player) -> None:
#         self.name = name
#         self.ui = ui
#         self.player = player

#     def _ensure_data(self):
#         if not hasattr(self, "_data"):
#             self._data = dict()

#     def _setup_influence(self, influence: Effect):
#         self._data[influence] = {"auto assign": RotatingDecision()}
 
#     def set_initial_link(self,  influence: Effect) -> None:
#         self._ensure_data()
#         self._setup_influence(influence)


#     def set_decision(self, pre_outcome: Outcome, decision_text: str, post_outcome: Outcome, next_outcome: Optional[Outcome] = None) -> None:
#         _vaild_arguments(pre_outcome, post_outcome, next_outcome)
#         self.set_initial_link(pre_outcome)

#         vaild_decision = self._data.get(pre_outcome)
#         try:
#             an_option = vaild_decision.get("auto assign").next_decision()
#         except StopIteration:
#             raise Exception(f"Limit was reached! Max limit is ({len(Decision)}) differetn outcomes!")
        
#         vaild_decision[an_option] = {"text": decision_text, "outcome": post_outcome, "linked": next_outcome}

#         if next_outcome:
#             self._setup_influence(next_outcome)


    # def _ensure_next_event(self):
    #     if not hasattr(self, "next_influence"):
    #         raise Exception("No starting event was set!")

    # def determine_players_outcome(self, current_influence: Effect) -> Optional[Effect]:
    #     self._ensure_data()
    #     # create error for not finshing adding dicisions to all events
    #     for event_data in self._data.values():
    #         if not any([event_data.get(d) for d in Decision]):
    #             raise Exception("An event was linked to another event. However, wan't properly filled out!")

    #     self.ui.display_text(current_influence.text)
    #     options = dict()
    #     for dicision in Decision:
    #         outcome = self._data.get(current_influence).get(dicision)
    #         if outcome:
    #             print("valid input ", dicision.name) # Temp Line
    #             utils.action_adder(options, dicision.name, outcome)

    #     player_dicision = self.ui.interact_with_user(options)
    #     self.ui.display_text(player_dicision.get("outcome").text)
    #     player_dicision.get("outcome").modify_player(self.player)
    #     return player_dicision.get("linked")
        

    # def __iter__(self):
    #     return self

    # def __next__(self):
    #     self._ensure_next_event()
    #     current_influence = self.next_influence
    #     self.next_influence = self.determine_players_outcome(current_influence)
    #     if self.next_influence == None:
    #         raise StopIteration
    #     return current_influence


def main():
    import View.cli as cli
    from pprint import pprint
    from Model.economy import Currency

    # cart = BrokenCart()
    # hunt = BridHunt()
    # events = [cart, hunt]
    # event = random.choice(events)

    # player = Player(name="bob")
    # ui = cli.CLI()

    # pre_outcome1 = Outcome(text="You were walking down a path and see a carriage with a broken wheel on the side of the road. ")
    # post_outcome1 = Outcome(text="After spending a few hours fixing the carriage. " \
    #                             "A old man steps out of the carriage and thanks you for fixing his carriage. " \
    #                             "He gives you 2 small gold coins. ", 
    #                         effect=ReceiveReward(item=Currency.Gold, amount=2))

    # # e2 = Effect("event_2")

    # s = Event(name="test", ui=ui, player=player)
    # s.set_initial_link(influence=pre_outcome1)
    # s.set_decision(pre_outcome1, "test is here", post_outcome1)
    # # s.set_decision(e2,"text is here", Outcome(text="player got damaged", effect=TakenDamage(damage=3)))
    # # for _ in s:
    # #     pass
    # # print(player.hp)
    # pprint(s._data)

    # # print({x:2 for x in range(10)})


if __name__ == "__main__":
    main()
