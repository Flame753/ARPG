from dataclasses import dataclass, field
from items import BaseItem
import slots
import setting


@dataclass() 
class Creature():
    def __init__(self):
        self.head = slots.Head()
        self.body = slots.Body()
        self.legs = slots.Legs()
        self.one_handed = slots.OneHanded()
        self.two_handed = slots.TwoHanded()
        self.inventory = slots.Miscellaneous()
        self.coin = slots.Coins()

    def _verifyArguments(self, item=None, amount=None):
        # Verifys if Arguments are enter correctly 
        if item:
            if not isinstance(item, BaseItem):
                raise TypeError(f'The item argument requires to be a BaseItem Object, not a {type(item)}!')
        if amount:
            if not type(amount) == int:
                raise TypeError(f'The amount argurment requires to be a intger, not a {type(amount)}!')
            if amount < 0:
                raise ValueError("The amount argurment can't be an negative real number!")
        if type(item) in [list, dict, tuple] or type(amount) in [list, dict, tuple]:
            raise TypeError(f"Arguments can't be a empty List, Dictionary or Tuple")

    def addItem(self, item: BaseItem, amount: int=1):
        self._verifyArguments(item, amount)

        # Always adds the amount of items into the invenotry slot excluding any Coin items
        if item.slot_type == setting.COIN_SLOT:
            self.coin.addItem(item, amount)
        else:
            self.inventory.addItem(item, amount)

    def removeItem(self, item: BaseItem, amount: int=1) -> bool:
        self._verifyArguments(item, amount)

        if item.slot_type == setting.COIN_SLOT:
            return self.coin.removeItem(item, amount)
        else:
            return self.inventory.removeItem(item, amount)

    def equip(self, item: BaseItem) -> bool:
        self._verifyArguments(item)
        # Verifying if there is an item to equip
        if not item in self.inventory.container:
            # No items to equip
            return False
        for slot in self.__dict__.values():
            # Finds proper slot for item
            if slot.type == item.slot_type:
                try:
                    # Adds item and checks if item was added
                    slot.addItem(item, 1)
                except IndexError:
                    # Capacity was reached
                    return False
                else:
                     # removes item from default inventory
                    self.removeItem(item, 1)
                    return True

    def unequip(self, item: BaseItem) -> bool:
        self._verifyArguments(item)

        for slot in self.__dict__.values():
            # Slots to Ignore 
            if slot.type in [setting.MISC_SLOT, setting.COIN_SLOT]: continue
            if slot.type == item.slot_type:
                # perventing any new/more items to be added if there was no items remove
                if slot.removeItem(item, 1):
                    self.addItem(item, 1)
                    return True
        return False
    
    def calculateItemWorth(self, item):
        self._verifyArguments(item)

        # Calcuates the total worth for the item, regarding where it is on the "Creature"
        worth = 0
        for slot in self.__dict__.values():
            # Verify a slot is a slot type
            if not isinstance(slot, slots.Slot): continue
            # Checks if item in the inventory or if equipped
            if item.slot_type == slot.type or slot.type == setting.MISC_SLOT:
                worth += slot.calculateItemWorth(item)
        return worth

    def calculateTotalWorth(self) -> int:
        # Calcuates the total worth of all coin and items regarding where it is on the "Creature"
        worth = 0
        for slot in self.__dict__.values():
            if not isinstance(slot, slots.Slot): continue
            worth += slot.calculateTotalWorth()
        return worth

    # def getAllItems(self) -> tuple[BaseItem, dict]:
    #     items = {}

    #     for data in self.inventory.values():
    #         slot = data['slot']
    #         items.update(slot.inventory)
    #     return items.items()

    def is_alive(self) -> bool:
        return self.hp > 0
  



def main():
    import items
    h = Creature()

    d = items.Dagger()
    b = items.Bread()
    # b = items.Backpack()

    h.addItem(d, 5)
    print(h.getAllItems())
    # h.addItem(items.Backpack())
    # print(h.getAllItems())
    for i, data in h.inventory.items():
        print(data['slot'].inventory)
    print('_________________')
    h.equipped(d)
    for i, data in h.inventory.items():
        print(data['slot'].inventory)
    print('_________________')
    # h.equipped(items.Dagger())
    # for i, data in h.inventory.items():
    #     print(data['slot'].inventory)
    # print('_________________')
    h.unequipped(d)
    for i, data in h.inventory.items():
        print(data['slot'].inventory)
    print('_________________')

    print(h.calculateTotalWorth())
    # print(h.addItem(items.Backpack()))
    # print(h.one_hand.inventory, h.body.inventory)
    # print(h.findItem(d))
    # print(h.calculateTotalWeight())
    # h.equipped(b)
    h.addItem(items.GoldCoin(), 23)
    print(h.getSlot('Coin').inventory)

def main2():
    import items
    from pprint import pprint
    c = Creature()

    ig1 = items.GoldCoin()
    ig2 = items.GoldCoin()
    d = items.Dagger()
    e = items.Dagger()
    # print(ig1 == ig2)
    # print(ig1 is ig2)
    # c.addItem(ig1)
    c.addItem(d, 4)
    c.addItem(e, 5)
    pprint(c)
    print(c.equip(d))
    pprint(c)
    print(c.equip(d))
    pprint(c)
    print(c.calculateTotalWorth())
    print(c.calculateItemWorth(d))
    # c.equip(ig1)
    # c.equip(d)
    # pprint(c)
    # c.unequip(d)
    # pprint(c)
    # c.equip(items.Dagger())
    # pprint(c)
    

    dagger = items.Dagger()
    copper_coin = items.CopperCoin()
    bread = items.Bread()

    creature = Creature()
    creature.addItem(bread, 3)
    pprint(creature)

def main3():
    import items
    c1 = Creature()
    c2 = Creature()

    print(c1 == c2)
    print(c1 is c2)
    print(c1.head == c2.head)
    print(c1.head is c2.head)
    cc = items.CopperCoin()
    c1.addItem(items.Dagger())
    c1.addItem(cc, 8)
    print(c1.removeItem(cc, 3))
    print(c1.coin)
    print(c1.inventory)


if __name__ == '__main__':
    main3()