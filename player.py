import items
import world
from creatures import Creature
from inventory import Inventory


class Player(Creature, items.Container):
    def __init__(self):
        self.inventory = Inventory(bag = items.Backpack())

        self.x = world.start_tile_location[0]
        self.y = world.start_tile_location[1]
        self.hp = 100
        self.max_hp = 100
        self.gold = 5
        self.victory = False

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def print_inventory(self):
        print("Inventory:")
        for item, amount in self.inventory.bag.inventory.items():
            amount = amount['amount']
            print(f'* {amount} {item}')
            best_weapon = self.most_powerful_weapon()
        print(f"Your best weapon is your {best_weapon}")
        print(f"Gold: {self.gold}")

    def most_powerful_weapon(self):
        max_damage = 0
        best_weapon = None
        for item in self.inventory.bag.inventory.keys():
            try:
                if item.damage > max_damage:
                    best_weapon = item
                    max_damage = item.damage
            except AttributeError:
                pass
        return best_weapon

    def attack(self):
        best_weapon = self.most_powerful_weapon()
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        print(f"You use {best_weapon.name} against {enemy.name}!")
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print(f"You killed {enemy.name}!")
        else:
            print(f"{enemy.name} HP is {enemy.hp}.")

    def heal(self):
        consumables = [(item, amount['amount']) for item, amount in self.inventory.bag.inventory.items() if isinstance(item, items.Consumable)]
        if not consumables:
            print("You don't have any items to heal you!")
            return
        
        print(f"Current HP {self.hp}")
        print("Choose an item to use to heal: ")
        for i, item in enumerate(consumables, 1):
            print(f"{i}. {item[1]} {item[0]}")
        
        valid = False
        while not valid:
            choice = input("")
            try:
                if choice == 0:  # Preventing accidentally using the last item 
                    print("Invalid choice, try again.")
                else:
                    to_eat = consumables[int(choice) - 1][0]
                    self.hp = min(self.max_hp, self.hp + to_eat.healing_value)
                    self.inventory.bag.removeItem(to_eat, 1)
                    print('')
                    print(f"Now Current HP: {self.hp}")
                    valid = True
            except (ValueError, IndexError):
                print("Invalid choice, try again.")

    def trade(self):
        room = world.tile_at(self.x, self.y)     
        room.check_if_trade(self)

def GeneratePlayer():
    # Adds the starting equipment to the player
    starting_equipment = {items.Rock(): 3,
                        items.Dagger(): 1,
                        items.Bread(): 2}
    player = Player()
    player.inventory.addItemsToBag(starting_equipment)
    return player

if __name__ == "__main__":
    world.parse_world_dsl()
    p = GeneratePlayer()
    p.heal()
    p.heal()
    print(p.bag.inventory)