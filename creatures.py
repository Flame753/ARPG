from abc import ABC
from items import BaseItem, Container
import slots


class Creature():
    def __init__(self, **kwargs):
        # if type(self) == Creature:
        #     raise NotImplementedError('Do not instantiate Creature directly')
        self.head = slots.Head()
        self.body = slots.Body()
        self.legs = slots.Legs()
        self.one_hand = slots.OneHand()
        self.two_hands = slots.TwoHands()
        self.small_items = slots.SmallItem()
        self.coins = slots.Coins()

    def findProperSlot(self, item: BaseItem) -> dict[slots.Slot]:
        # Returns the slot location of the item.
        for slot in self.__dict__.values():
            if not isinstance(slot, slots.Slot): continue
            if slot.name == item.slot:
                return slot

    def addItem(self, item: BaseItem, amount: int=1) -> bool:
        slot = self.findProperSlot(item)
        # Determining if capacity was reached
        if slot.amountOfItems() + amount > slot.item_limit:
            raise IndexError(f"Added {amount} of {item} is exceeding the limited of {slot.item_limit}")
        if isinstance(item, Container): item.updateSlotLimit(self, amount)
        slot.addItem(item, amount)

    def removeItem(self, item: BaseItem, amount: int=1) -> bool:
        slot = self.findProperSlot(item)
        if isinstance(item, Container): item.updateSlotLimit(self, amount, negative=True)
        return slot.removeItem(item, amount)

    def calculateTotalWeight(self) -> int:
        weight = 0
        for slot in self.__dict__.values():
            if not isinstance(slot, slots.Slot): continue
            weight = weight + slot.calculateItemWeight()
        return weight

    def calculateTotalWorth(self) -> int:
        worth = 0
        for slot in self.__dict__.values():
            if not isinstance(slot, slots.Slot): continue
            worth = worth + slot.calculateItemWorth()
        return worth

    def findItem(self, item:BaseItem) -> dict[slots.Slot]:
        # Finds a specific item in the creature's inventory then returns the slot location of the item.
        for slot in self.__dict__.values():
            if not isinstance(slot, slots.Slot): continue
            slot.ensureInventory()
            if slot.inventory.get(item, None): 
                return slot
        return None

    def getAllItems(self) -> tuple[BaseItem, dict['Amount']]:
        items = {}
        for slot in self.__dict__.values():
            if not isinstance(slot, slots.Slot): continue
            slot.ensureInventory()
            items.update(slot.inventory)
        return items.items()

    def is_alive(self) -> bool:
        return self.hp > 0
    


if __name__ == '__main__':
    import items
    h = Creature()

    d = items.Dagger()
    b = items.Backpack()

    h.addItem(items.Dagger(), 2)
    print(h.getAllItems())
    h.addItem(items.Backpack())
    print(h.getAllItems())

    # print(h.addItem(items.Backpack()))
    # print(h.one_hand.inventory, h.body.inventory)
    # print(h.findItem(d))
    # print(h.calculateTotalWeight())