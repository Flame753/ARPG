# Standard library imports 
import enum
from dataclasses import dataclass, field
from itertools import count

# Local application imports
from Model.outcome_effects import Effect, Outcome, OUTCOME_EFFECTS, OutcomeEffects
from Model.economy import Currency
from Model.utils import Color


situation_id_counter = count(0, 1)
ReceiveItem = OUTCOME_EFFECTS.get(OutcomeEffects.ReceiveItem)
LoseHealth = OUTCOME_EFFECTS.get(OutcomeEffects.LoseHealth)


@dataclass
class Situation:
    id: str = field(repr=False, init=False)
    text: str = ""

    def __post_init__(self):
        self.id = str(situation_id_counter.__next__())


@dataclass
class Event:
    situation: Situation = field(default_factory=Situation)
    options: list[str] = field(default_factory=list)
    outcomes: list[Outcome] = field(default_factory=list)

    def set_situation(self, text: str):
        self.situation.text = text

    def add_outcome(self, options: str, outcome: Outcome):
        self.options.append(options)
        self.outcomes.append(outcome)


def BrokenCart():
    e = Event()
    situation = "You were walking down a path and see a carriage with a broken wheel on the side of the road. "
    option1 = "Do you stop and help repaire the carriage? "
    option2 = "Or, continue on your journey. "
    outcome1 = Outcome(result="After spending a few hours fixing the carriage. " \
                            "A old man steps out of the carriage and thanks you for fixing his carriage. " \
                            "He gives you 2 small gold coins. ",
                        effect=ReceiveItem(item=Currency.Gold, amount=2))
    outcome2 = Outcome(result="You mind your own business and pass the traveler. Nothing happens. ")

    e.set_situation(situation)
    e.add_outcome(option1, outcome1)
    e.add_outcome(option2, outcome2)
    return e

def BridHunt(color):
    e = Event()
    template = "You see a flock of {color} bird flying over head. " \
                "It seem like a great change to get a easy meal. "

    option1 = "Shot one down. "
    option2 = "Let them fly pass you. "

    if color == Color.Red:
        situation = template.format(color=Color.Red.name.lower())
        damage_amount = 2
        outcome1 = Outcome(result="After taking aim and releasing your arrow. " \
                                "However, you notice it wasn't a flock of birds. " \
                                f"But, a flock of {color.name} wyverns. " \
                                f"You have suffered {damage_amount} damage! ",
                            effect=LoseHealth(damage_amount))
        outcome2 = Outcome(result="You let the flock of bird fly pass you. " \
                                "Nothing else eventful happened. ")
    elif color == Color.White:
        situation = template.format(color=Color.White.name.lower())
        outcome1 = Outcome(result="After taking aim and releasing your arrow. " \
                                "It hits your mark and you made a great meal out of your hunt. " \
                                "Nothing else happened that day. ")
        outcome2 = Outcome(result="You let the flock of bird fly pass you. " \
                                "Nothing else eventful happened. ")
    else:
        raise ValueError("Incorrect value was entered for this function. " \
                        "Check perimeter value if it's a type of color. ")

    e.set_situation(situation)
    e.add_outcome(option1, outcome1)
    e.add_outcome(option2, outcome2)
    return e

def breakingtest():
    e = Event()
    situation = "Testing!"
    option1 = "option1"
    option2 = "option2"
    option3 = "option3"
    option4 = "option4"
    outcome1 = Outcome(result="outcome1")
    outcome2 = Outcome(result="outcome2")
    outcome3 = Outcome(result="outcome3")
    outcome4 = Outcome(result="outcome4")

    e.set_situation(situation)
    e.add_outcome(option1, outcome1)
    e.add_outcome(option2, outcome2)
    e.add_outcome(option3, outcome3)
    e.add_outcome(option4, outcome4)
    return e


class RoadEvents(enum.Enum):
    BrokenCart = BrokenCart()
    BridHunt_White = BridHunt(Color.White)
    BridHunt_Red = BridHunt(Color.Red)
    bad = breakingtest()
