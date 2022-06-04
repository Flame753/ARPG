# Standard library imports 
from collections import OrderedDict
import enum

# Local application imports
from View.ui import UI, ValidActions
from View.cli import CLI
from Model.player import Player
import Model.story_pieces as story_pieces
from Model.book import Chapter


def action_adder(action_dict, hotkey, action):
        action_dict[hotkey.lower()] = action

def interact_with_player(ui: UI, actions: ValidActions):
    ui.display_actions(actions)
    player_input = ui.get_user_input()
    vaild_action = actions.get(player_input.lower())
    if vaild_action:
        vaild_action()
    else:
        ui.display_invalid_input(player_input=player_input)



class Game:
    def __init__(self, ui: UI, player: Player) -> None:
        self.ui = ui
        self.active = True
        self.player = player
        self.world = "World"
        self.title = f"The Adventure of Ether"
    
    def main_menu(self) -> dict:
        actions = OrderedDict()

        if self.world:
            action_adder(actions, "create", self.play)
        if None:
            action_adder(actions, "resume", self.play)
        if None:
            action_adder(actions, "save", self.save)
        
        action_adder(actions, "exit", self.exit)
        
        return actions

    def exit(self):
        self.save()
        self.active = False

    def save(self):
        "Saving the Game"

    def run(self):
        self.ui.display_title(self.title)

        while self.active:
            interact_with_player(self.ui, actions=self.main_menu())
            
    def play(self):
        road_events = [event.BridHunt(), event.BrokenCart()]
        scenarios = []
        ch1 = Chapter(road_events=road_events, scenarios=scenarios)
        
        while self.player.is_alive():
            ch1.run_random_road_event(ui=self.ui, player=self.player)
            
            # interact_with_player(self.ui, actions=self.main_menu())
            break




def main():
    cli = CLI()
    player = Player("Sam")
    game = Game(cli, player)
    game.run()


if __name__ == "__main__":
    main()