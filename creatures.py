from items import BaseItem
import slots


# class Creature():
#     def __init__(self, **kwargs):
#         # if type(self) == Creature:
#         #     raise NotImplementedError('Do not instantiate Creature directly')
#         self.head = slots.Head()
#         self.body = slots.Body()
#         self.legs = slots.Legs()
#         self.one_hand = slots.OneHand()
#         self.two_hands = slots.TwoHands()
#         self.small_items = slots.SmallItem()
#         self.coins = slots.Coins()

#     def findProperSlot(self, item: BaseItem) -> dict[slots.Slot]:
#         # Returns the slot location of the item.
#         for slot in self.__dict__.values():
#             if not isinstance(slot, slots.Slot): continue
#             if slot.properSlot(item):
#                 return slot

#     def preventDuplicate(self, item: BaseItem) -> BaseItem:
#         # Prevent Duplicates in slots
#         slot = self.findProperSlot(item)
#         slot.ensureInventory()
#         if slot.inventory:
#             for i in slot.inventory:
#                 if i.name == item.name:
#                     return i
#         return item

#     def addItem(self, item: BaseItem, amount: int=1) -> bool:
#         item = self.preventDuplicate(item)
#         slot = self.findProperSlot(item)
#         if isinstance(item, Container): item.updateSlotLimit(self, amount)
#         slot.addItem(item, amount)

#     def removeItem(self, item: BaseItem, amount: int=1) -> bool:
#         slot = self.findProperSlot(item)
#         if isinstance(item, Container): item.updateSlotLimit(self, amount, negative=True)
#         return slot.removeItem(item, amount)

#     def calculateTotalWeight(self) -> int:
#         weight = 0
#         for slot in self.__dict__.values():
#             if not isinstance(slot, slots.Slot): continue
#             weight = weight + slot.calculateItemWeight()
#         return weight

#     def calculateTotalWorth(self) -> int:
#         worth = 0
#         for slot in self.__dict__.values():
#             if not isinstance(slot, slots.Slot): continue
#             worth = worth + slot.calculateItemWorth()
#         return worth

#     def findItem(self, item:BaseItem) -> dict[slots.Slot]:
#         # Finds a specific item in the creature's inventory then returns the slot location of the item.
#         for slot in self.__dict__.values():
#             if not isinstance(slot, slots.Slot): continue
#             slot.ensureInventory()
#             if slot.inventory.get(item, None): 
#                 return slot
#         return None

#     def getAllItems(self) -> tuple[BaseItem, dict]:
#         items = {}
#         for slot in self.__dict__.values():
#             if not isinstance(slot, slots.Slot): continue
#             slot.ensureInventory()
#             items.update(slot.inventory)
#         return items.items()

#     def is_alive(self) -> bool:
#         return self.hp > 0

class Creature():
    def __init__(self, **kwargs):
        # if type(self) == Creature:
        #     raise NotImplementedError('Do not instantiate Creature directly')
        head = slots.Head()
        body = slots.Body()
        legs = slots.Legs()
        one_hand = slots.OneHand()
        two_hands = slots.TwoHands()
        coins = slots.Coins()
        other = slots.Miscellaneous()

        self.inventory = {head.name: {'slot': head, 'item_limit': 1},
                        body.name: {'slot': body, 'item_limit': 1},
                        legs.name: {'slot': legs, 'item_limit': 1},
                        one_hand.name: {'slot': one_hand, 'item_limit': 1},
                        two_hands.name: {'slot': two_hands, 'item_limit': 1},
                        coins.name: {'slot': coins, 'item_limit': None},
                        other.name: {'slot': other, 'item_limit': None}}

    def preventDuplicate(self, item: BaseItem) -> BaseItem:
        # Prevent Duplicates Items
        slots = []
        slots.append(self.inventory['Miscellaneous']['slot'])

        # Prevents Duplicate if an item starts equippted 
        # None is means items has no slot type
        data = self.inventory.get(item.slot, None)
        if data:
            slots.append(data['slot'])

        for slot in slots:
            slot.ensureInventory()
            if slot.inventory:
                for i in slot.inventory:
                    # NEEDS TO CHECK MORE THEN JUST NAME TO BE FULLY WORKING
                    if i.name == item.name:
                        return i
        return item

    def addItem(self, item: BaseItem, amount: int=1):
        item = self.preventDuplicate(item)
        if item.slot == 'Coin':
            slot = self.getSlot('Coin')
        else:
            slot = self.getSlot('Miscellaneous')
        slot.addItem(item, amount)

    def removeItem(self, item: BaseItem, amount: int=1) -> bool:
        item = self.preventDuplicate(item)
        slot = self.inventory['Miscellaneous']['slot']
        return slot.removeItem(item, amount)
            
    def equipped(self, item: BaseItem):
        item = self.preventDuplicate(item)
        data = self.inventory.get(item.slot, None)

        # "not data" looks for items that dosen't have a specific slot type like a bread object
        if not data:
            raise KeyError(f"'{item}' is not equiptable Object!")
        slot = data['slot']

        # "not limit" checks if there is no item slot limit like a coin object
        limit= data['item_limit']
        if not limit:
            raise ValueError(f"'{item}' is not equiptable Object!!")

        if slot.amountOfItems() >= limit:
            raise IndexError(f"{slot} is Fully Occupied!")

        slot.addItem(item, 1)
        self.removeItem(item, 1)

    def unequipped(self, item: BaseItem) -> bool:
        item = self.preventDuplicate(item)
        data = self.inventory.get(item.slot, None)
        slot = data['slot']
        if not slot:
            raise KeyError(f"This {slot} Doesn't Exist!")

        self.addItem(item, 1)
        return slot.removeItem(item, 1)  

    def getSlot(self, slot: str) -> slots.Slot:
        return self.inventory[slot]['slot']

    # def calculateTotalWeight(self) -> int:
    #     weight = 0
    #     for slot in self.__dict__.values():
    #         if not isinstance(slot, slots.Slot): continue
    #         weight = weight + slot.calculateItemWeight()
    #     return weight

    def calculateTotalWorth(self) -> int:
        worth = 0
        for data in self.inventory.values():
            slot = data['slot']
            worth = worth + slot.calculateTotalWorth()
        return worth

    # def findItem(self, item:BaseItem) -> dict[slots.Slot]:
    #     # Finds a specific item in the creature's inventory then returns the slot location of the item.
    #     for slot in self.__dict__.values():
    #         if not isinstance(slot, slots.Slot): continue
    #         slot.ensureInventory()
    #         if slot.inventory.get(item, None): 
    #             return slot
    #     return None

    def getAllItems(self) -> tuple[BaseItem, dict]:
        items = {}

        for data in self.inventory.values():
            slot = data['slot']
            slot.ensureInventory()
            items.update(slot.inventory)
        return items.items()

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
if __name__ == '__main__':
    main()