import random
import enemies
import npc


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
    def __init__(self, x, y) -> None:
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
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.trader = npc.Trader()
    
    def trade(self, buyer, seller):
        selling_list = {}
        
        while True:
            seller_items = [(item, amount['amount']) for item, amount in seller.inventory.bag.inventory.items()]
            for i, item in enumerate(seller_items, 1):
                # Creating item list that can be traded
                selling_list.update({str(i): item[0]})
                # Listing seller's items for sale
                print(f'{i}. {item[1]} {item[0].name} - {item[0].worth} Gold')

            user_input = input("Choose an item or press Q to exit: ")
            if user_input in ['Q', 'q']: 
                return
            else:
                choice = user_input
                to_swap = selling_list.get(choice)
                if to_swap:
                    self.swap(seller, buyer, to_swap)
                else:
                    print("Invalid Choice!")

    def swap(self, seller, buyer, item):
        if not seller.inventory.bag.inventory:
            if isinstance(seller, npc.NonPlayableCharacter):
                print('Seller has ran out of stock of items.')
            else:
                print('You have ran out of things to sell.')
            return
        if item.worth > buyer.gold:
            print("That's too expensive")
            return
        seller.inventory.bag.removeItem(item, 1)
        buyer.inventory.bag.addItem(item, 1)
        seller.gold = seller.gold + item.worth
        buyer.gold  = buyer.gold - item.worth
        print("Trade complete!")

        # Printing player's current gold amount
        text = 'You Currenlty have {} Gold.'
        if not isinstance(seller, npc.NonPlayableCharacter):
            print(text.format(seller.gold))
        else:
            print(text.format(buyer.gold))

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

class FindGoldTile(MapTile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.gold = random.randint(1, 50)
        self.gold_claimed = False
    
    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.gold = player.gold + self.gold
            print("+{} gold added.".format(self.gold))
    
    def intro_text(self):
        if self.gold_claimed:
            return """
            Another unremarkable part of the cave. You must forge onwards.
            """
        else:
            return """
            Someone dropped some gold. You pick it up.
            """

world_map = []
start_tile_location = None

tile_type_dict = {"VT": VictoryTile,
                    "EN": EnemyTile,
                    "ST": StartTile,
                    "FG": FindGoldTile,
                    "TT": TraderTile,
                    "  ": None}

world_dsl = """
|EN|EN|VT|EN|EN|
|EN|  |  |  |EN|
|EN|FG|EN|  |TT|
|TT|  |ST|FG|EN|
|FG|  |EN|  |FG|
"""

def tile_at(x, y):
    """
    Returns the a specific tile in the world map if exists
    """
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None

def is_dsl_valid(dsl):
    # There should be exactly one start tile
    if dsl.count("|ST|") != 1:
        return False

    # There should be at least one victory tile    
    if dsl.count("|VT|") == 0:
        return False

    # Each row should have the same number of cells
    lines = dsl.splitlines()
    lines = [l for l in lines if l]  # Removes any empty strings
    pipe_counts = [line.count("|") for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False
    
    return True

def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError("DSL is invalid!")

    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]
    for y, dsl_row in enumerate(dsl_lines):
        # Create an object to store the tiles
        row = []
        # Split the line into abbreviations using the "split method"
        dsl_cells = dsl_row.split("|")
        # The split method includes the beginning and end of the line
        # so we need to remove those nonexistent cells
        dsl_cells = [c for c in dsl_cells if c]
        # Iterate over each cell in the DSL line 
        # Instead of j, the variable x is used because 
        # we're working with an X-Y grid.
        for x, dsl_cell in enumerate(dsl_cells):
            # Look up the abbreviation in the dictionary
            tile_type = tile_type_dict[dsl_cell]
            if tile_type == StartTile:
                # Setting the player at starting tile
                global start_tile_location
                start_tile_location = x, y
            # If the dictionary returned a vaild type, create 
            # a new tile object, pass it the X-Y coordinates
            # as required by the tile __init__(), and add
            # it to the row object. If None was found in the 
            # dictionary, we just add None.
            row.append(tile_type(x, y) if tile_type else None)
        #Add the whole row io the world_map
        world_map.append(row)
