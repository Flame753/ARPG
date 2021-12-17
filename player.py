import items
import world
from creatures import Creature

class Player(Creature):
    def __init__(self) -> None:
        self.inventory = [items.Rock(), items.Dagger(), items.Bread(), items.Bread()]

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
        for item in self.inventory:
            print('*' + str(item))
            best_weapon = self.most_powerful_weapon()
        print(f"Your best weapon is your {best_weapon}")
        print(f"Gold: {self.gold}")

    def most_powerful_weapon(self):
        max_damage = 0
        best_weapon = None
        for item in self.inventory:
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
        consumables = [item for item in self.inventory if isinstance(item, items.Consumable)]
        if not consumables:
            print("You don't have any items to heal you!")
            return
        
        print(f"Current HP {self.hp}")
        print("Choose an item to use to heal: ")
        for i, item in enumerate(consumables, 1):
            print(f"{i}. {item}")
        
        valid = False
        while not valid:
            choice = input("")
            try:
                if choice == 0:  # Preventing accidentally using the last item 
                    print("Invalid choice, try again.")
                else:
                    to_eat = consumables[int(choice) - 1]
                    self.hp = min(self.max_hp, self.hp + to_eat.healing_value)
                    self.inventory.remove(to_eat)
                    print('')
                    print(f"Now Current HP: {self.hp}")
                    valid = True
            except (ValueError, IndexError):
                print("Invalid choice, try again.")

    def trade(self):
        room = world.tile_at(self.x, self.y)     
        room.check_if_trade(self)


