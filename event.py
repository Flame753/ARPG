# Standard library imports 
from dataclasses import dataclass, field, fields, astuple
from typing import Optional
import random
import enum

# Local application imports
from player import Player
from ui import UI
import utils


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


@dataclass(frozen=True)
class Effect():
    result_text: str

    def add_requirement(self, requirement) -> None:
        if not hasattr(requirement, "requirement"):
            self.requirement = [requirement]
        else:
            self.requirement.append(requirement)
        
    def modify_player(self, player: Player) -> None:
        pass

@dataclass(frozen=True)
class PlayerTakesDamage(Effect):
    damage: int

    def modify_player(self, player: Player) -> None:
        player.hp -= self.damage

@dataclass(frozen=True)
class PlayerRestoresHealth(PlayerTakesDamage):
    def modify_player(self, player: Player) -> None:
        player.hp += self.damage
        if player.hp > player.max_hp:
            player.hp = player.max_hp

@dataclass(frozen=True)
class ReceiveReward(Effect):
    item: str
    amount: int

    def modify_player(self, player: Player) -> None:
        player.add_item(self.item, self.amount)

@dataclass(frozen=True)
class LossItem(ReceiveReward):
    def modify_player(self, player: Player) -> None:
        player.remove_item(self.item, self.amount)


def _vaild_arguments(influence: Effect, outcome: Effect, next_influence: Optional[Effect]) -> None:
    if not isinstance(influence, Effect):
        raise TypeError(f"{influence} unvalid argument for the influence perimeter!")
    if not isinstance(outcome, Effect):
        raise TypeError(f"{outcome} unvalid argument for the outcome perimeter!")
    if not isinstance(next_influence, (Effect, type(None))):
        raise TypeError(f"{next_influence} unvalid argument for the next_influence perimeter!")


@dataclass
class Event:
    def __init__(self, name: str, ui: UI, player: Player) -> None:
        self.name = name
        self.ui = ui
        self.player = player

    def _ensure_data(self):
        if not hasattr(self, "_data"):
            self._data = dict()

    def _setup_event(self, influence: Effect):
        self._data[influence] = {"auto assign": RotatingDecision()}
 
    def set_starting_link(self,  influence: Effect) -> None:
        self._ensure_data()
        if self._data:
            raise Exception("This method was already once used!")
        self._setup_event(influence)
        self.next_influence = influence

    def set_decision(self, influence: Effect, outcome: Effect, next_influence: Optional[Effect]=None):
        _vaild_arguments(influence, outcome, next_influence)

        if not hasattr(self, "_data"):
            raise Exception("<set_starting_link must be called before this method is called!>")

        event_decision = self._data.get(influence)
        if event_decision == None:
            raise Exception(f"The entered influence <{influence}> doesn't exist! Try linking this event with an existing event, first!")

        try:
            option = event_decision.get("auto assign").next_decision()
        except StopIteration:
            raise Exception(f"Limit was reached! Max limit is ({len(Decision)}) differetn outcomes!")
        
        event_decision[option] = {"outcome": outcome, "linked_influence": next_influence}

        if next_influence:
            self._setup_event(next_influence)


    def _ensure_next_event(self):
        if not hasattr(self, "next_influence"):
            raise Exception("No starting event was set!")

    def determine_players_outcome(self, current_influence: Effect) -> Optional[Effect]:
        self._ensure_data()
        # create error for not finshing adding dicisions to all events
        for event_data in self._data.values():
            if not any([event_data.get(d) for d in Decision]):
                raise Exception("An event was linked to another event. However, wan't properly filled out!")

        self.ui.display_text(current_influence.result_text)
        options = dict()
        for dicision in Decision:
            outcome = self._data.get(current_influence).get(dicision)
            if outcome:
                print("valid input ", dicision.name) # Temp Line
                utils.action_adder(options, dicision.name, outcome)

        player_dicision = self.ui.interact_with_user(options)
        self.ui.display_text(player_dicision.get("outcome").result_text)
        player_dicision.get("outcome").modify_player(self.player)
        return player_dicision.get("linked_influence")
        

    def __iter__(self):
        return self

    def __next__(self):
        self._ensure_next_event()
        current_influence = self.next_influence
        self.next_influence = self.determine_players_outcome(current_influence)
        if self.next_influence == None:
            raise StopIteration
        return current_influence



def BrokenCart() -> Event:
    into_text: str = "You were walking down a path and see a carriage with a broken wheel on the side of the road. "

    options = {Decision.A.name: Option(context="Do you stop and help repaire the carriage? ",
                                outcomes=[ReceiveReward(text="After spending a few hours fixing the carriage. " \
                                                            "A old man steps out of the carriage and thanks you for fixing his carriage. " \
                                                            "He gives you 2 small gold coins. ",
                                                        item=Currency.Gold,
                                                        amount=2),
                                        PlayerTakesDamage(text="After, getting closing to the carriage. " \
                                                "Suddenly, two bandits jump out from the carriage. " \
                                                "You fight the bandits off. " \
                                                "However, you have suffer some damage from the bandits. ",
                                                damage=2)]),
            Decision.B.name: Option(context="Or, continue on your journey. ",
                            outcomes=[Outcome(text="You mind your own business and pass the traveler. Nothing happens. ")])}

    return Event(into_text=into_text, options=options)


def main():
    import cli
    from pprint import pprint
    from economy import Currency

    # cart = BrokenCart()
    # hunt = BridHunt()
    # events = [cart, hunt]
    # event = random.choice(events)

    player = Player(name="bob")
    ui = cli.CLI()

    Influence1 = Effect("You were walking down a path and see a carriage with a broken wheel on the side of the road. ")
    outcome1 = ReceiveReward(result_text="After spending a few hours fixing the carriage. " \
                                                            "A old man steps out of the carriage and thanks you for fixing his carriage. " \
                                                            "He gives you 2 small gold coins. ", item=Currency.Gold, amount=2)
    e2 = Effect("event_2")

    s = Event(name="test", ui=ui, player=player)
    s.set_starting_link(influence=Influence1)
    s.set_decision(Influence1, outcome1, e2)
    s.set_decision(e2, PlayerTakesDamage(result_text="player got damaged", damage=3))
    for _ in s:
        pass
    print(player.hp)
    pprint(s._data)

    # print({x:2 for x in range(10)})


if __name__ == "__main__":
    main()
