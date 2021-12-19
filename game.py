from collections import OrderedDict
from player import GeneratePlayer
import world

def play():
    print("Escape from Cave Terror!")
    world.parse_world_dsl()
    player = GeneratePlayer()
        
    while player.is_alive() and not player.victory:
        room = world.tile_at(player.x, player.y)
        text_separator()
        print(room.intro_text())
        text_separator()
        room.modify_player(player)  # Enemy attacks player first

        if player.is_alive() and not player.victory:
            choose_action(room, player)
        elif not player.is_alive():
            print("Your journey has come to an early end!")
            
def get_available_actions(room, player):
    """
    Returns a dictionary of functions that are valid action.
    """
    actions = OrderedDict()
    print("Choose an action: ")
    if player.bag.inventory:
        action_adder(actions, 'i', player.print_inventory, "Print Inventory")
    if isinstance(room, world.TraderTile):
        action_adder(actions, 't', player.trade, "Trade")
    if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
        action_adder(actions, 'a', player.attack, "Attack")
    else:
        if world.tile_at(room.x, room.y - 1):
            action_adder(actions, 'n', player.move_north, "Go north")
        if world.tile_at(room.x, room.y + 1):
            action_adder(actions, 's', player.move_south, "Go south")
        if world.tile_at(room.x + 1, room.y):
            action_adder(actions, 'e', player.move_east, "Go east")
        if world.tile_at(room.x - 1, room.y):
            action_adder(actions, 'w', player.move_west, "Go west")
    if player.hp < player.max_hp:
        action_adder(actions, 'h', player.heal, "Heal")
    
    return actions 

def action_adder(action_dict, hotkey, action, name):
    action_dict[hotkey.lower()] = action
    action_dict[hotkey.upper()] = action
    print("{}: {}".format(hotkey, name))

def choose_action(room, player):
    """
    Allows the player to pick valid action during the game.
    """
    action = None
    while not action:
        available_actions = get_available_actions(room, player)
        action_input = input("Action: ")
        print('')
        action = available_actions.get(action_input)
        if action:
            action()
        else:
            print("Invalid action!")

def text_separator():
    print("-"*100)


if __name__ == '__main__':
    play()