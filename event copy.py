# Standard library imports 
from dataclasses import dataclass, field, fields, astuple
import random
import enum
from re import X

# Local application imports
from player import Player
from ui import UI
from economy import Currency


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


@dataclass
class Event():
    into_text: str = field(repr=False)
    options: dict[Decision: Option] = field(default_factory=dict, repr=False)

    def get_outcome(self, player_decision: Decision) -> str:
        option = self.options.get(player_decision)
        if option:
            return option.get_random_outcome()
        else:
            raise InvalidInput(f"Invalid Input was entered: {player_decision}")

    def run_event(self, ui: UI, player: Player):
        ui.display_text(self.into_text)
        
        while True:
            for decision, text in self.options.items():
                ui.display_text(f"{decision}: {text.context}")

            player_input = ui.get_player_input()

            try:
                outcome = self.get_outcome(player_input.upper())
                ui.display_text(outcome.text)
                outcome.modify_player(player)
                break
            except InvalidInput:
                ui.display_invalid_input(player_input)



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


def BridHunt() -> Event:
    into_text: str = "You see a flock of bird flying over head. " \
                    "It seem like a great change to get a easy meal. "

    options = {Decision.A.name: Option(context="Shot a it down.",
                                outcomes=[Outcome(text="After taking aim and releasing your arrow. " \
                                                        "It hits your mark and you made a great meal out of your hunt. " \
                                                        "Nothing else happened that day. ")]),
            Decision.B.name: Option(context="Let it fly pass you. ",
                                outcomes=[Outcome(text="You let the flock of bird fly pass you. " \
                                                                "Nothing else eventful happened. ")])}
    return Event(into_text=into_text, options=options)



def main():
    import cli

    # cart = BrokenCart()
    # hunt = BridHunt()
    # events = [cart, hunt]
    # event = random.choice(events)
    # player = Player(name="bob")
    # ui = cli.CLI()

    # event.run_event(ui, player)

    # # Testing
    # print(f"your current HP is {player.hp}")
    # player._ensure_inventory()
    # print("Your inventory: ", player._inventory)
    # a = Decision
    # for x in range(10):
    #     print(next(a.decision_next()))


    # def gen():
    #     for x in Decision:
    #         yield x
    # a = gen()
    # print(next(a))
    # print(next(a))
    # print(next(a))
    # print(next(gen()))
    # print(next(gen()))



if __name__ == "__main__":
    main()
