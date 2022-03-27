# Standard library imports 
from operator import eq
from pprint import pprint

# Local application imports
from entities import creatures
from world import tiles
from entities import items
from entities import currency



class Player(creatures.Creature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.x = tiles.start_tile_location[0]
        self.y = tiles.start_tile_location[1]
        self.victory = False

        self.add_item(items.Dagger())
        self.add_item(items.Bread())
        self.add_item(currency.SilverCoin(), 3)
        # self.add_item(items.CoinPouch(sellable=False))

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
        print("-"*15 + "Inventory" + "-"*15)

        for slot_name, equipment_slot in self.equipment.items():
            equipment_slot._ensure_inventory()
            print(f"{slot_name.capitalize()}:")
            if not equipment_slot.inventory:
                print("* None\n")
            else:
                for items, amount in equipment_slot.inventory.items():
                    print(f"* {amount['amount']} {items.name}\n")
                    

        print("Equipped Items:")
        for armor_slot in self.equippable.values():
            armor_slot._ensure_inventory()
            for items, amount in armor_slot.inventory.items():
                print(f"* {amount['amount']} {items.name}")

        best_equipped_weapon = self.most_powerful_equipped_weapon()
        best_weapon = self.most_powerful_weapon()
        if best_equipped_weapon:
            print(f"Your best equipped weapon is your {best_weapon.name}!")
        else: 
            print(f"Your best weapon is your {best_weapon.name}, you might want to equip it!")

    def most_powerful_equipped_weapon(self):
        max_damage = 0
        best_weapon = None
        weapons = [self.get_slot(creatures.ONE_HANDED), self.get_slot(creatures.TWO_HANDED)]
        for weapon in weapons:
            weapon._ensure_inventory()
            for item in weapon.inventory.keys():
                if not hasattr(item, 'damage'): continue
                if item.damage > max_damage:
                    best_weapon = item
                    max_damage = item.damage
        return best_weapon

    def most_powerful_weapon(self):
        max_damage = 0
        best_weapon = None
        weapons = [self.get_slot(creatures.ONE_HANDED), self.get_slot(creatures.TWO_HANDED), self.get_slot(creatures.WEAPONS)]
        for weapon in weapons:
            weapon._ensure_inventory()
            for item in weapon.inventory.keys():
                if not hasattr(item, 'damage'): continue
                if item.damage > max_damage:
                    best_weapon = item
                    max_damage = item.damage
        return best_weapon

    def attack(self):
        best_weapon = self.most_powerful_weapon()
        room = tiles.tile_at(self.x, self.y)
        enemy = room.enemy
        print(f"You use {best_weapon.name} against {enemy.name}!")
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print(f"You killed {enemy.name}!")
        else:
            print(f"{enemy.name} HP is {enemy.hp}.")

    def heal(self):
        consumables = [(item, amount['amount']) for item, amount in self.get_slot(creatures.CONSUMABLES).inventory.items()]
        if not consumables:
            print("You don't have any items to heal you!")
            return
        
        print(f"Current HP {self.hp}")
        print("Choose an item to use to heal: ")
        for i, item in enumerate(consumables, 1):
            print(f"{i}. {item[1]} {item[0].name}")
        
        valid = False
        while not valid:
            choice = input("")
            try:
                if choice == 0:  # Preventing accidentally using the last item 
                    print("Invalid choice, try again.")
                else:
                    to_eat = consumables[int(choice) - 1][0]
                    self.hp = min(self.max_hp, self.hp + to_eat.healing_value)
                    self.remove_item(to_eat, 1)
                    print('')
                    print(f"Now Current HP: {self.hp}")
                    valid = True
            except (ValueError, IndexError):
                print("Invalid choice, try again.")

    def equip(self):
        pass

    def unequip(self):
        pass

    def trade(self):
        room = tiles.tile_at(self.x, self.y)     
        room.check_if_trade(self)


def main():
    # def GeneratePlayer():
    #     # Adds the starting equipment to the player
    #     starting_equipment = {items.Rock(): 3,
    #                         items.Dagger(): 1,
    #                         items.Bread(): 2}
    #     player = Player()
    #     for item, amount in starting_equipment.items():
    #         player.add_item(item, amount)
    #     return player
    tiles.parse_world_dsl()
    player = Player()
    # best = player.most_powerful_weapon()
    # print(best)
    # player.print_inventory()
    pprint(player.get_slot(creatures.COINS).inventory)
    player.equip(items.Dagger())
    player.print_inventory()


if __name__ == "__main__":
    main()
