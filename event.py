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


@dataclass
class Outcome():
    text: str

    def modify_player(self, player: Player) -> None:
        pass

@dataclass
class PlayerTakesDamage(Outcome):
    damage: int

    def modify_player(self, player: Player) -> None:
        player.hp -= self.damage

@dataclass
class ReceiveReward(Outcome):
    item: str
    amount: int

    def modify_player(self, player: Player) -> None:
        player.add_item(self.item, self.amount)

@dataclass
class LossItem(ReceiveReward):
    def modify_player(self, player: Player) -> None:
        player.remove_item(self.item, self.amount)


@dataclass
class Option:
    context: str
    outcomes: list[Outcome]

    def get_random_outcome(self) -> Outcome:
        return random.choice(self.outcomes)


@dataclass(frozen=True)
class Event():
    into_text: str = field(repr=False)
    # options: dict[Decision: Option] = field(default_factory=dict, repr=False)

    # def get_outcome(self, player_decision: Decision) -> str:
    #     option = self.options.get(player_decision)
    #     if option:
    #         return option.get_random_outcome()
    #     else:
    #         raise InvalidInput(f"Invalid Input was entered: {player_decision}")


def _vaild_arguments(existing_event: Event, outcome: Outcome, next_event: Optional[Event]) -> None:
    if not isinstance(existing_event, Event):
        raise TypeError(f"{existing_event} unvalid argument for the existing_event perimeter!")
    if not isinstance(outcome, Outcome):
        raise TypeError(f"{outcome} unvalid argument for the outcome perimeter!")
    if not isinstance(next_event, (Event, type(None))):
        raise TypeError(f"{next_event} unvalid argument for the next_event perimeter!")


@dataclass
class Scenario:
    def __init__(self, name: str, ui: UI, player: Player) -> None:
        self.name = name
        self.ui = ui
        self.player = player

    def _ensure_data(self):
        if not hasattr(self, "_data"):
            self._data = dict()

    def _setup_event(self, event: Event):
        self._data[event] = {"auto assign": RotatingDecision()}
 
    def set_starting_event(self,  event: Event) -> None:
        self._ensure_data()
        if self._data:
            raise Exception("This method was already once used!")
        self._setup_event(event)
        self.next_event = event

    def set_decision(self, existing_event: Event, outcome: Outcome, next_event: Optional[Event]=None):
        _vaild_arguments(existing_event, outcome, next_event)

        if not hasattr(self, "_data"):
            raise Exception("<set_starting_event must be called before this method is called!>")

        event_decision = self._data.get(existing_event)
        if event_decision == None:
            raise Exception(f"The entered event <{existing_event}> doesn't exist! Try linking this event with an existing event, first!")

        try:
            option = event_decision.get("auto assign").next_decision()
        except StopIteration:
            raise Exception(f"Limit was reached! Max limit is ({len(Decision)}) differetn outcomes!")
        
        event_decision[option] = {"outcome": outcome, "linked_event": next_event}

        if next_event:
            self._setup_event(next_event)


    def _ensure_next_event(self):
        if not hasattr(self, "next_event"):
            raise Exception("No starting event was set!")

    def determine_players_outcome(self, current_event: Event) -> Optional[Event]:
        self._ensure_data()
        # create error for not finshing adding dicisions to all events
        self.ui.display_text(current_event.into_text)
        options = dict()
        for dicision in Decision:
            outcome = self._data.get(current_event).get(dicision)
            if outcome:
                print("valid input ", dicision.name) # Temp Line
                utils.action_adder(options, dicision.name, outcome)

        player_dicision = self.ui.interact_with_user(options)
        self.ui.display_text(player_dicision.get("outcome").text)
        return player_dicision.get("linked_event")
        

    def __iter__(self):
        return self

    def __next__(self):
        self._ensure_next_event()
        current_event = self.next_event
        self.next_event = self.determine_players_outcome(current_event)
        if self.next_event == None:
            raise StopIteration
        return current_event



def main():
    import cli

    # cart = BrokenCart()
    # hunt = BridHunt()
    # events = [cart, hunt]
    # event = random.choice(events)

    # player = Player(name="bob")
    # ui = cli.CLI()

    # e1 = Event("event_1")
    # e2 = Event("event_2")

    # s = Scenario(name="test", ui=ui, player=player)
    # s.set_starting_event(event=e1)
    # s.set_decision(e1, PlayerTakesDamage(text="player got damaged", damage=3), e2)
    # s.set_decision(e2, PlayerTakesDamage(text="player got damaged", damage=3))
    # for _ in s:
    #     pass

    print({x:2 for x in range(10)})



if __name__ == "__main__":
    main()
