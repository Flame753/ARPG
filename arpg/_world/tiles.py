from entities import enemies
from entities import npc
from entities import items
import random


class MapTile:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def intro_text(self):
        raise NotImplementedError("Create a subclass instead!")

    def modify_player(self, player):
        pass

class StartTile(MapTile):
    def intro_text(self):
        return """
        You find yourself in a cave with a flickering torch on the wall.
        You can make out four paths, each equally as dark and foreboding.
        """

class BoringTile(MapTile):
    def intro_text(self):
        return """
        This is a very boring part of the cave.
        """

class VictoryTile(MapTile):
    def modify_player(self, player):
        player.victory = True

    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!
        Victory is yours!
        """

class EnemyTile(MapTile):
    def __init__(self, x, y):
        super().__init__(x,y)
        r = random.random()
        if r < 0.50:
            self.enemy = enemies.GiantSpider()
            self.alive_text = "A giant spider jumps down from " \
                                "its web in front of you!"
            self.dead_text = "The corpse of a dead spider " \
                                "rots on the ground."
        elif r < 0.80:
            self.enemy = enemies.Ogre()
            self.alive_text = "An ogre is blocking your path!"
            self.dead_text = "A dead ogre reminds you of your triumph."
        elif r < 0.90:
            self.enemy = enemies.BatColony()
            self.alive_text = "You hear a squeaking noise growing louder" \
                                "...suddenly you are lost in a swarm of bats!"
            self.dead_text = "Dozens of dead bats are scattered on the ground." 
        else:
            self.enemy = enemies.RockMonster()
            self.alive_text = "You've disturbed a rock monster " \
                                "from is slumber!"
            self.dead_text = "Defeated, the monster has reverted " \
                                "into an ordinary rock."
    
    def intro_text(self):
        if self.enemy.is_alive(): text = self.alive_text
        else: text = self.dead_text
        return text
    
    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, player.hp))

class TraderTile(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.trader = npc.Trader()
        self.items_on_sell = {}
    
    def trade(self, seller, buyer):
        while True:
            for i, item in enumerate(seller.inventory.container.keys(), start=1):
                amount = seller.inventory.container.get(item)['amount']
                print(f"{i}. {item.name} - {item.worth} copper (amount: {amount})")
                self.items_on_sell[str(i)] = item

            user_input = input("Choose an item or press Q to exit: ")
            if user_input in ['Q', 'q']: 
                return
            else:
                choice = user_input
                to_swap = self.items_on_sell.get(choice)
                if to_swap:
                    self.swap(seller, buyer, to_swap)
                else:
                    print("Invalid Choice!")

    def swap(self, seller, buyer, item):
        # seller's inventory is empty
        if not self.items_on_sell:
            if isinstance(seller, npc.NonPlayableCharacter):
                print('Seller has ran out of stock of items.')
            else:
                print('You have ran out of things to sell.')
            return

        # Verifying that the buyer has enough cash to buy the item
        if item.worth > buyer.coin_pouch.calculateTotalWorth():
            print("That's too expensive")
            return

        # Where exchanging items happen
        # Buyer.addItem can return expection if buyer has no space for item
        try:
            # Where exchanging coins happen
            if not self.transaction(seller, buyer, item):
                print(f"Transaction incomplete! No Trade!")
                return
            buyer.addItem(item, 1)
            seller.removeItem(item, 1)
            print("Trade complete!")
        except IndexError:
            if isinstance(buyer, npc.NonPlayableCharacter):
                print('Buyer has reached thier carring capacity.')
            else:
                print(f'You have reached your carring capacity.')

        # Prints the player's coins
        def display_coins(player):
            print('You currenlty have;')
            player.coin_pouch.order()
            for coin, amount in player.coin_pouch.container.items():
                amount = amount['amount']
                print(f'    {amount} {coin.name}')

        if not isinstance(seller, npc.NonPlayableCharacter):
            # Player is the seller
            display_coins(seller)
        else:
            # Playser is the buyer
            display_coins(buyer)
        print('-'*20)

    def transaction(self, seller, buyer, item):
        price = item.worth
        buyer_weight = buyer.coin_pouch.calculateTotalWorth()

        if not isinstance(seller, npc.NonPlayableCharacter):
            # Player is the seller
            seller.addItem(items.CopperCoin(), item.worth)
            return True
        else:
            # Playser is the buyer
            # Need to figure out how to do this part
            return True
        return False

    def check_if_trade(self, player):
        while True:
            print("Would you like to (B)uy, (S)ell or (Q)uit?")
            user_input = input()
            if user_input in ['Q', 'q']:
                return
            elif user_input in ['B', 'b']:
                print("Here's whats available to buy: ")
                self.trade(buyer=player, seller=self.trader)
            elif user_input in ['S', 's']:
                print("Here's whats available to sell: ")
                self.trade(buyer=self.trader, seller=player)
            else:
                print("Invalid choice!")

    def intro_text(self):
        return """
        A frail not-quite-human, not-quite-creature squats in the corner
        clinking his gold coins together. He looks willing to trader.
        """

class FindCoinTile(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.coins_claimed = False
        # self.coins_remainding = False
        r = random.random()
        if r < 0.75:
            self.coin = items.CopperCoin() 
            self.amount = random.randint(1, 50)
        elif r < 0.9:
            self.coin = items.SilverCoin()
            self.amount = random.randint(1, 25)
        elif r < 0.99:
            self.coin = items.GoldCoin()
            self.amount = random.randint(1, 10)
        else:
            self.coin = items.PlatinumCoin()
            self.amount = random.randint(1, 5)
    
    def modify_player(self, player):
        if not self.coins_claimed:
            player.coin_pouch.addItem(self.coin, self.amount)
            print(f"You have picked {self.amount} {self.coin}s.")
            self.coins_claimed = True

    def intro_text(self):
        if self.coins_claimed:
            return """
            Another unremarkable part of the cave. You must forge onwards.
            """
        else:
            return f"""
            You found {self.amount} {self.coin}s!
            """


