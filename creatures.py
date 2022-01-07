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

    def properSlot(self, slot: slots.Slot, item: BaseItem) -> bool:
       return True if item.slot == slot.name else False

    def addItem(self, slot: slots.Slot, item: BaseItem, amount: int=1) -> bool:
        if self.properSlot(slot, item):
            slot.addItem(item, amount)
            return True
        return False

    def removeItem(self, slot: slots.Slot, item: BaseItem, amount: int=1) -> bool:
        if self.properSlot(item, slot):
            slot.removeItem(item, amount)
            return True
        return False

    def calculateTotalWeight(self):
        weight = 0
        for slot in self.__dict__.values():
            slot.ensureInventory()
            for item, data in slot.inventory.items():
                weight += item.weight * data['amount']
        return weight

    def calculateTotalWorth(self):
        worth = 0
        for slot in self.__dict__.values():
            slot.ensureInventory()
            for item, data in slot.inventory.items():
                worth += item.worth * data['amount']
        return worth

    def findItem(self, item:BaseItem) -> dict[slots.Slot]:
        # Finds a specific item in the creature's inventory then returns the slot location of the item.
        for slot in self.__dict__.values():
            slot.ensureInventory()
            if slot.inventory.get(item, None): 
                return slot
        return None

    def is_alive(self):
        return self.hp > 0
    


if __name__ == '__main__':
    import items
    h = Creature()

    d = items.Dagger()
    b = items.Backpack()
    # starting_equipment = {items.Rock(): 3,
    #                 d: 1,
    #                 items.Bread(): 2,
    #                 b: 1}
    # for k, v in starting_equipment.items():
    #     pass
    print(h.head)
    print(h.addItem(h.head, d))
    print(h.addItem(h.one_hand, d))
    print(h.findItem(d))
    print(h.calculateTotalWeight())