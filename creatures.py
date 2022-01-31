from optparse import AmbiguousOptionError
from items import BaseItem
from dataclasses import dataclass, field
import slots
import setting


@dataclass() 
class Creature():
    head: slots.Slot = slots.Head()
    body: slots.Slot = slots.Body()
    legs: slots.Slot = slots.Legs()
    one_handed: slots.Slot = slots.OneHanded()
    two_handed: slots.Slot = slots.TwoHanded()
    inventory: slots.Slot = slots.Miscellaneous()
    coin: slots.Slot = slots.Coins()

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


    def addItem(self, item: BaseItem, amount: int=1):
        self._verifyArguments(item, amount)

        # Always adds the amount of items into the invenotry slot excluding any Coin items
        if item.slot_type == setting.COIN_SLOT:
            self.coin.addItem(item, amount)
        else:
            self.inventory.addItem(item, amount)

    def removeItem(self, item: BaseItem, amount: int=1) -> bool:
        self._verifyArguments(item, amount)
        
        return self.inventory.removeItem(item, amount)

    def equip(self, item: BaseItem):
        self._verifyArguments(item)

        for slot in self.__dict__.values():
            # Finds proper slot for item
            if slot.type == item.slot_type:
                # Adds item and checks if item was added
                if slot.addItem(item, 1):
                    # removes item from default inventory
                    self.removeItem(item, 1)

    def unequip(self, item: BaseItem) -> bool:
        self._verifyArguments(item)

        for slot in self.__dict__.values():
            if slot.type == item.slot_type:
                if slot.removeItem(item, 1):
                    self.addItem(item, 1)
    
    def calculateItemWorth(self, item):
        self._verifyArguments(item)

        # Calcuates the total worth for the item, regarding where it is on the "Creature"
        worth = 0
        for slot in self.__dict__.values():
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


if __name__ == '__main__':
    main2()