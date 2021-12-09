class Weapon:
    def __init__(self) -> None:
        raise NotImplementedError("Do not create raw Weapon objects.")

    def __str__(self) -> str:
        return self.name

class Rock(Weapon):
    def __init__(self) -> None:
        self.name = 'Rock'
        self.description = "A fist-sized rock, suitable for bludgeoning."
        self.damage = 5

class Dagger(Weapon):
    def __init__(self) -> None:
        self.name = "Dagger"
        self.description = "A small dagger with some rust. " \
                            "Somewhat more dangerous than a rock."
        self.damage = 10

class RustySword(Weapon):
    def __init__(self) -> None:
        self.name = "Rusty sword"
        self.description = "This sword is showing its age, " \
                            "but still has some fight in it."
        self.damage = 20

class Crossbow(Weapon):
    def __init__(self) -> None:
        self.name = "Crossbow"
        self.description = "Strong and sturdy Crossbow." \
                            "Allows a range attack."
        self.damage = 15

class Axe(Weapon):
    def __init__(self) -> None:
        self.name = "Axe"
        self.description = "This axe is showing its age, " \
                            "but still has some fight in it to do damage."
        self.damage = 25

def get_player_command():
    return input('Action: ')

def play():
    inventory = [Rock(), Dagger(), 'Gold(5)', "Crusty Bread"]
    print("Escape from Cave Terror!")
    while True:
        action_input = get_player_command()
        if action_input in ['n', 'N']:
            print("Go North!")
        elif action_input in ['s', 'S']:
            print("Go South!")
        elif action_input in ['e', 'E']:
            print("Go East!")
        elif action_input in ['w', 'W']:
            print("Go West!")
        elif action_input in ['i', 'I']:
            print("Inventory:")
            for item in inventory:
                print('*' + str(item))
        elif action_input in ['q', 'Q']:
            break
        else:
            print("Invalid action!")

def most_powerful_weapon(inventory):
    max_damage = 0
    best_weapon = None
    for item in inventory:
        try:
            if item.damage > max_damage:
                best_weapon = item
                max_damage = item.damage
        except AttributeError:
            pass
    return best_weapon


if __name__ == '__main__':
    play()