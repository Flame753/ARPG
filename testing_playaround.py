# Introspection based solution
from ast import Pass
from dataclasses import astuple, dataclass, fields


# @dataclass
# class Point:
#     x: float
#     y: float
#     z: float

#     def __add__(self, other):
#         # return Point(*(getattr(self, dim.name)+getattr(other, dim.name) for dim in fields(self)))

#         print( *(getattr(self, dim.name)-getattr(other, dim.name) for dim in fields(self)))

#     def __sub__(self, other):
#         return Point(*(getattr(self, dim.name)-getattr(other, dim.name) for dim in fields(self)))

#     def __mul__(self, other):
#         return Point(*(getattr(self, dim.name)*other for dim in fields(self)))

#     def __rmul__(self, other):
#         return self.__mul__(other)

#     def __iter__(self):
#         return iter(astuple(self))

# a = Point(1,2,3) - (Point(1,1,1))
# print(a)
# for p in Point(1,1,2):
#     print(p)


# class Event:

#     def __init__(self) -> None:
#         self.lit = list((2,3,2,5,1,23,5))
#         self.pointer = 0
    
#     def __iter__(self):
#         return self
    
#     def __next__(self): 
#         self.pointer += 1
#         if self.pointer >= len(self.lit):
#             self.pointer = 0
#             raise StopIteration
#         print(self.lit)
#         return self.lit[self.pointer]


class Event:

    def __init__(self) -> None:
        self.lit = list((2,3,2,5,1,23,5))
        self.pointer = 0
    
    def __iter__(self):
        return iter(self.lit)
    
    # def __next__(self): 
    #     self.pointer += 1
    #     if self.pointer >= len(self.lit):
    #         self.pointer = 0
    #         raise StopIteration
    #     print(self.lit)
    #     return self.lit[self.pointer]


# a = Event()
# for x in a:
#     print(x)

# print("test")
# for x in a:
#     print(x)

from dataclasses import dataclass, field, fields, astuple
from event import Decision, Outcome, RotatingDecision
from typing import Optional
import enum
from ui import UI
from player import Player

# @dataclass
# class Decision():
#     A: int = 1
#     B: int = 2
#     C: int = 3



# print(dir(Decision.A))
# print(Decision.A)



class NonEquippableError(Exception):
    """Exception raised for non-equippable item was used."""
    
    def __init__(self, message="Non-Equippable Items are not supported!"):
        self.message = message
        super().__init__(self.message)

def _vaild_arguments(existing_event: Event, decision: Decision, outcome: Outcome, next_event: Optional[Event]) -> None:
    if not isinstance(existing_event, Event):
        raise TypeError(f"{existing_event} unvalid argument for the existing_event perimeter!")
    if not isinstance(decision, Decision):
        raise TypeError(f"{decision} unvalid argument for the decision perimeter!")
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

    def __iter__(self):
        return self

    def __next__(self):
        self._ensure_data()
        if not hasattr(self, "next_event"):
            raise Exception("No starting event was set!")
        self.current_event = self.next_event
        # Might no work becuause Event class needs to be reworked
        player_dicision = self.current_event.run_event(ui=self.ui, player=self.player)
        self.next_event = self._data.get(self.current_event).get(player_dicision).get("linked_event")
        return self.current_event

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
        # _vaild_arguments(existing_event, decision, outcome, next_event)

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
        
    def get_next_event(self):
        pass


from pprint import pprint
s = Scenario("ui")
s.set_starting_event("Burn Event")
print(s._data)
s.set_decision("Burn Event", outcome="hi", next_event="Fire Storm")
pprint(s._data)
s.set_decision("Burn Event", outcome="Sing")
pprint(s._data)
s.set_decision("Fire Storm", outcome="Fire")
pprint(s._data)
s.set_decision("Fire Storm", outcome="water")
pprint(s._data)
s.set_decision("Fire Storm", outcome="wind", next_event="Blue Flame")
pprint(s._data)
# s.set_decision("Fire Storm", outcome="sky")
# pprint(s._data)
# s.set_decision("Frozen Event", outcome="hi")
# pprint(s._data)

for x in s:
    print(x)
