# Standard library imports 
from collections import OrderedDict
import enum

# Local application imports
from View.ui import UI
from View.cli import CLI
from Model.player import Player, create_player
from Model.story_pieces import RoadEvents
import Controller.engine as eng 


# def action_adder(action_dict, hotkey, action):
#         action_dict[hotkey.lower()] = action

# def interact_with_player(ui: UI, actions):
#     ui.display_actions(actions)
#     player_input = ui.get_user_input()
#     vaild_action = actions.get(player_input.lower())
#     if vaild_action:
#         vaild_action()
#     else:
#         ui.display_invalid_input(player_input=player_input)



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
            eng.action_adder(actions, "create", self.play)
        if None:
            eng.action_adder(actions, "resume", self.play)
        if None:
            eng.action_adder(actions, "save", self.save)
        
        eng.action_adder(actions, "exit", self.exit)
        
        return actions

    def exit(self):
        self.save()
        self.active = False

    def save(self):
        "Saving the Game"

    def run(self):
        self.ui.display_title(self.title)

        while self.active:
            eng.GameEngine.interact_with_player(self.ui, actions=self.main_menu())
            
    def play(self):
        road_events = [RoadEvents.BridHunt.value, RoadEvents.BrokenCart.value]
        # scenarios = []
        # ch1 = Chapter(road_events=road_events, scenarios=scenarios)
        
        while self.player.is_alive():
            for event in road_events:
                eng.EventEngine.interact_with_player(self.ui, self.player, event)
            # ch1.run_random_road_event(ui=self.ui, player=self.player)
            
            # interact_with_player(self.ui, actions=self.main_menu())
            break




def main():
    cli = CLI()
    player = create_player("Sam")
    game = Game(cli, player)
    game.run()


if __name__ == "__main__":
    main()