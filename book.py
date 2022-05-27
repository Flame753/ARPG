# Standard library imports 
from dataclasses import dataclass, field
import random

# Local application imports
from event import Event, InvalidInput
from player import Player
from ui import UI


def testing(player):
    print(f"your current HP is {player.hp}")
    player._ensure_inventory()
    print("Your inventory: ", player._inventory)



@dataclass
class Chapter:
    road_events: list[Event] = field(default_factory=list)
    city_events: list[Event] = field(default_factory=list)
    scenarios: list = field(default_factory=list)

    def run_random_road_event(self, ui: UI, player: Player):
        random.choice(self.road_events).run_event(ui, player)

    def run_random_city_event(self, ui: UI, player: Player):
        random.choice(self.city_events).run_event(ui, player)

    def remove_event(self, event: Event) -> None:
        self.events.remove(event)

    def add_event(self, event: Event) -> None:
        self.events.append(event)

    def run_random_scenario(self):
        pass


def main():
    import cli
    import event
    ui = cli.CLI()
    player = Player("Tom")
    road_events = [event.BridHunt(), event.BrokenCart()]
    scenarios = []
    ch1 = Chapter(road_events=road_events, scenarios=scenarios)
    ch1.run_random_road_event(ui=ui, player=player)
    


if __name__ == "__main__":
    main()
