from ast import Pass
from items import BaseItem
from dataclasses import dataclass, field
from container import Container
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

    def addItem(self, item: BaseItem, amount: int=1):
        if item.slot_type == setting.COIN_SLOT:
            self.coin.addItem(item, amount)
        else:
            self.inventory.addItem(item, amount)

    def removeItem(self, item: BaseItem, amount: int=1) -> bool:
        return self.inventory.removeItem(item, amount)

    def equipped(self, item: BaseItem):
        slot = self.equipment_slots.get(item.slot, None)
        if slot:
            slot.equip(item)
            self.removeItem(item, 1)

    def unequipped(self, item: BaseItem) -> bool:
        slot = self.equipment_slots.get(item.slot)
        slot.unequip(item)
        self.addItem(item, 1)

    def calculateTotalWorth(self) -> int:
        worth = self.inventory.calculateTotalWorth()

        for slot in self.equipment_slots.values():
            
            worth += slot.inventory.calculateTotalWorth()
        return worth
    
    


    # def preventDuplicate(self, item: BaseItem) -> BaseItem:
    #     # Prevent Duplicates Items
    #     slots = []
    #     slots.append(self.inventory['Miscellaneous']['slot'])

    #     # Prevents Duplicate if an item starts equippted 
    #     # None is means items has no slot type
    #     data = self.inventory.get(item.slot, None)
    #     if data:
    #         slots.append(data['slot'])

    #     for slot in slots:
    #         if slot.inventory:
    #             for i in slot.inventory:
    #                 # NEEDS TO CHECK MORE THEN JUST NAME TO BE FULLY WORKING
    #                 if i.name == item.name:
    #                     return i
    #     return item

    # def addItem(self, item: BaseItem, amount: int=1):
    #     item = self.preventDuplicate(item)
    #     if item.slot == 'Coin':
    #         slot = self.getSlot('Coin')
    #     else:
    #         slot = self.getSlot('Miscellaneous')
    #     slot.addItem(item, amount)

    # def removeItem(self, item: BaseItem, amount: int=1) -> bool:
    #     item = self.preventDuplicate(item)
    #     slot = self.inventory['Miscellaneous']['slot']
    #     return slot.removeItem(item, amount)
            
    # def equipped(self, item: BaseItem):
    #     item = self.preventDuplicate(item)
    #     data = self.inventory.get(item.slot, None)

    #     # "not data" looks for items that dosen't have a specific slot type like a bread object
    #     if not data:
    #         raise KeyError(f"'{item}' is not equiptable Object!")
    #     slot = data['slot']

    #     # "not limit" checks if there is no item slot limit like a coin object
    #     limit= data['item_limit']
    #     if not limit:
    #         raise ValueError(f"'{item}' is not equiptable Object!!")

    #     if slot.amountOfItems() >= limit:
    #         raise IndexError(f"{slot} is Fully Occupied!")

    #     slot.addItem(item, 1)
    #     self.removeItem(item, 1)

    # def unequipped(self, item: BaseItem) -> bool:
    #     item = self.preventDuplicate(item)
    #     data = self.inventory.get(item.slot, None)
    #     slot = data['slot']
    #     if not slot:
    #         raise KeyError(f"This {slot} Doesn't Exist!")

    #     self.addItem(item, 1)
    #     return slot.removeItem(item, 1)  

    # def getSlot(self, slot: str) -> slots.Slot:
    #     return self.inventory[slot]['slot']

    # # def calculateTotalWeight(self) -> int:
    # #     weight = 0
    # #     for slot in self.__dict__.values():
    # #         if not isinstance(slot, slots.Slot): continue
    # #         weight = weight + slot.calculateItemWeight()
    # #     return weight

    # def calculateTotalWorth(self) -> int:
    #     worth = 0
    #     for data in self.inventory.values():
    #         slot = data['slot']
    #         worth = worth + slot.calculateTotalWorth()
    #     return worth

    # def getAllItems(self) -> tuple[BaseItem, dict]:
    #     items = {}

    #     for data in self.inventory.values():
    #         slot = data['slot']
    #         items.update(slot.inventory)
    #     return items.items()

    # def is_alive(self) -> bool:
    #     return self.hp > 0



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
    d = Creature()
    # print(c)
    # print(c == d)
    # print(c is d)
    # print(c.head.container == d.inventory.container)
    # print(c.head.container is d.inventory.container)
    ig1 = items.GoldCoin()
    ig2 = items.GoldCoin()
    print(ig1 == ig2)
    print(ig1 is ig2)
    items.GoldCoin()
    c.addItem(ig1)
    pprint(c)
    print(c.removeItem(ig2))
    pprint(c)
 
if __name__ == '__main__':
    main2()