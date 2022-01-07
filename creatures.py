from abc import ABC
from items import BaseItem, Container
import slots


class Creature():
    def __init__(self, **kwargs):
        # if type(self) == Creature:
        #     raise Exception('Do not instantiate Creature directly')
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
        return None

    def addItem(self, item: BaseItem, amount: int=1) -> bool:
        slot = self.findProperSlot(item)
        if not slot: return False
        if isinstance(item, Container): item.updateSlotLimit(self, amount)
        return slot.addItem(item, amount)

    def removeItem(self, item: BaseItem, amount: int=1) -> bool:
        slot = self.findProperSlot(item)
        if not slot: return False
        if isinstance(item, Container): item.updateSlotLimit(self, amount, True)
        return slot.removeItem(item, amount)

    def calculateTotalWeight(self) -> int:
        weight = 0
        for slot in self.__dict__.values():
            if not isinstance(slot, slots.Slot): continue
            slot.ensureInventory()
            for item, data in slot.inventory.items():
                weight += item.weight * data['amount']
        return weight

    def calculateTotalWorth(self) -> int:
        worth = 0
        for slot in self.__dict__.values():
            if not isinstance(slot, slots.Slot): continue
            slot.ensureInventory()
            for item, data in slot.inventory.items():
                worth += item.worth * data['amount']
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

    print(h.addItem(items.Dagger()))
    print(h.addItem(items.Backpack()))
    print(h.one_hand.inventory, h.body.inventory)
    # print(h.findItem(d))
    # print(h.calculateTotalWeight())