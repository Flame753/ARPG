# Standard library imports 
import enum
from dataclasses import dataclass, field

# Local application imports
from Model.outcome_effects import Effect, Outcome, OUTCOME_EFFECTS, OutcomeEffects
from Model.economy import Currency


ReceiveReward = OUTCOME_EFFECTS.get(OutcomeEffects.ReceiveReward)


@dataclass
class Event:
    situation: str = ""
    options: list[str] = field(default_factory=list)
    outcomes: list[Effect] = field(default_factory=list)

    def set_into_text(self, text: str):
        self.situation = text

    def add_outcome(self, options: Outcome, outcomes: Outcome):
        self.options.append(options)
        self.outcomes.append(outcomes)


def BrokenCart():
    e = Event()
    situation = "You were walking down a path and see a carriage with a broken wheel on the side of the road. "
    option1 = "Do you stop and help repaire the carriage? "
    option2 = "Or, continue on your journey. "
    outcome1 = Outcome(result="After spending a few hours fixing the carriage. " \
                            "A old man steps out of the carriage and thanks you for fixing his carriage. " \
                            "He gives you 2 small gold coins. ",
                        effect=ReceiveReward(item=Currency.Gold, amount=2))
    outcome2 = Outcome(result="You mind your own business and pass the traveler. Nothing happens. ")

    e.set_into_text(situation)
    e.add_outcome(option1, outcome1)
    e.add_outcome(option2, outcome2)
    return e

def BridHunt():
    e = Event()
    situation = "You see a flock of bird flying over head. " \
                "It seem like a great change to get a easy meal. "
    option1 = "Shot a it down."
    option2 = "Let it fly pass you. "
    outcome1 = Outcome(result="After taking aim and releasing your arrow. " \
                            "It hits your mark and you made a great meal out of your hunt. " \
                            "Nothing else happened that day. ")
    outcome2 = Outcome(result="You let the flock of bird fly pass you. " \
                            "Nothing else eventful happened. ")

    e.set_into_text(situation)
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

    e.set_into_text(situation)
    e.add_outcome(option1, outcome1)
    e.add_outcome(option2, outcome2)
    e.add_outcome(option3, outcome3)
    e.add_outcome(option4, outcome4)
    return e


class RoadEvents(enum.Enum):
    BrokenCart = BrokenCart()
    BridHunt = BridHunt()
    bad = breakingtest()
