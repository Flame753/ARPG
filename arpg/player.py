# Standard library imports 
from pprint import pprint

# Local application imports
from entities.creatures import Creature
from world import tiles
from entities import items
from entities import currency



class Player(Creature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.x = tiles.start_tile_location[0]
        self.y = tiles.start_tile_location[1]
        self.victory = False

        self.addItem(items.Dagger())
        self.addItem(items.Bread())
        self.addItem(currency.SilverCoin(), 3)
        # self.addItem(items.CoinPouch(sellable=False))

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
        for item, amount in self.inventory.container.items():
            if isinstance(item, currency.Coin): continue
            amount = amount['amount']
            print(f'* {amount} {item.name}')
        best_weapon = self.most_powerful_weapon()
        print(f"Your best weapon is your {best_weapon.name}")

        print("Coins:")
        self.coin_pouch.order(reverse=True)
        for coin, amount in self.coin_pouch.container.items():
            amount = amount['amount']
            print(f'* {amount} {coin.name}')

    def most_powerful_weapon(self):
        max_damage = 0
        best_weapon = None
        for item in self.inventory.container.keys():
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
        consumables = [(item, amount['amount']) for item, amount in self.inventory.container.items() if isinstance(item, items.Consumable)]
        print(consumables)
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
                    self.removeItem(to_eat, 1)
                    print('')
                    print(f"Now Current HP: {self.hp}")
                    valid = True
            except (ValueError, IndexError):
                print("Invalid choice, try again.")

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
    #         player.addItem(item, amount)
    #     return player
    tiles.parse_world_dsl()
    player = Player()
    # best = player.most_powerful_weapon()
    # print(best)
    # player.print_inventory()
    pprint(player.inventory.container)
    pprint(player.coin_pouch.container)


if __name__ == "__main__":
    main()
