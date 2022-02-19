from abc import ABC, abstractmethod
from dataclasses import dataclass, field
# from container import Container
from items import BaseItem
import setting



@dataclass
class Container(ABC):
    container: dict = field(default_factory=dict, init=False)
    
    @abstractmethod
    def addItem(self, item, amount=0):
        pass

    @abstractmethod
    def removeItem(self, item, amount = 0):
        pass

    @abstractmethod
    def calculateItemWeight(self, item):
        pass

    @abstractmethod
    def calculateItemWorth(self, item):
        pass

    @abstractmethod
    def calculateTotalWeight(self):
        pass

    @abstractmethod
    def calculateTotalWorth(self):
        pass


@dataclass()
class Slot(Container):
    type: str = None
    item_limit: int = None
    
    def addItem(self, item: BaseItem, amount: int=0) -> bool:
        # Checks if there a limit or not
        if self.item_limit:
            # Check if limit was passed
            if len(self.container) >= self.item_limit: 
                raise IndexError(f"Exceeded Maximum Capacity of {self.item_limit}! Unable to add {item}!")
        # Adds another items if exist
        if item in self.container:
            self.container[item]['amount'] += amount
        # Adds new item
        else:
            self.container[item] = {'amount': amount}
    
    def removeItem(self, item, amount = 0):
        if item in self.container:
            if self.container[item]['amount'] >= amount:
                self.container[item]['amount'] -= amount
                if self.container[item]['amount'] == 0:
                    del(self.container[item])
                return True
        return False

    def calculateItemWeight(self, item):
        raise NotImplementedError()
        if item in self.container:
            return item.weight * self.container[item]['amount']
        return 0

    def calculateItemWorth(self, item):
        if item in self.container:
            return item.worth * self.container[item]['amount']
        return 0

    def calculateTotalWeight(self):
        raise NotImplementedError()
        weight = 0
        for item, data in self.container.items():
            weight += item.weight * data['amount']
        return weight

    def calculateTotalWorth(self):
        worth = 0
        for item, data in self.container.items():
            worth += item.worth * data['amount']
        return worth

@dataclass()
class Head(Slot):
    type: str = setting.HEAD_SLOT
    item_limit: int = 1

@dataclass()
class Body(Slot):
    type: str = setting.BODY_SLOT
    item_limit: int = 1

@dataclass()
class Legs(Slot):
    type: str = setting.LEGS_SLOT
    item_limit: int = 1

@dataclass()
class OneHanded(Slot):
    type: str = setting.ONE_HANDED_SLOT
    item_limit: int = 1
    
@dataclass()    
class TwoHanded(Slot):
    type: str = setting.TWO_HANDED_SLOT
    item_limit: int = 1

@dataclass()
class Coins(Slot):
    type: str = setting.COIN_SLOT

    def order(self) -> list:
        # Puts the container from largest worth to smallest
        coins = list(self.container.items())
        worth = lambda coin: coin[0].worth
        coins.sort(key=worth)  # Sort function only works with a list type
        ordict = dict(coins)
        self.container.clear()
        self.container.update(ordict)

@dataclass()
class Miscellaneous(Slot):
    type: str = setting.MISC_SLOT


class Inventory(Container):
    def __init__(self):
        super().__init__()
        self.container.update({setting.HEAD_SLOT: Head()})
        self.container.update({setting.BODY_SLOT: Body()})
        self.container.update({setting.LEGS_SLOT: Legs()})
        self.container.update({setting.ONE_HANDED_SLOT: OneHanded()})
        self.container.update({setting.TWO_HANDED_SLOT: TwoHanded()})
        self.container.update({setting.MISC_SLOT: Miscellaneous()})
        self.container.update({setting.COIN_SLOT: Coins()})


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
            coin = self.container.get(setting.COIN_SLOT)
            coin.addItem(item, amount)
        else:
            misc = self.container.get(setting.MISC_SLOT)
            misc.addItem(item, amount)

    def removeItem(self, item: BaseItem, amount: int=1) -> bool:
        self._verifyArguments(item, amount)

        if item.slot_type == setting.COIN_SLOT:
            coin = self.container.get(setting.COIN_SLOT)
            return coin.removeItem(item, amount)
        else:
            misc = self.container.get(setting.MISC_SLOT)
            return misc.removeItem(item, amount)

    def equip(self, item: BaseItem) -> bool:
        self._verifyArguments(item)
        misc = self.container.get(setting.MISC_SLOT)
        # Verifying if there is an item to equip
        if not item in misc.container:
            # No items to equip
            return False
        for slot in self.container.values():
            # Finds proper slot for item
            if slot.type == item.slot_type:
                try:
                    # Adds item and checks if item was added
                    slot.addItem(item, 1)
                except IndexError:
                    # Capacity was reached
                    return False
                else:
                     # removes item from default misc
                    self.removeItem(item, 1)
                    return True

    def unequip(self, item: BaseItem) -> bool:
        self._verifyArguments(item)

        for slot in self.container.values():
            # Slots to Ignore 
            if slot.type in [setting.MISC_SLOT, setting.COIN_SLOT]: continue
            if slot.type == item.slot_type:
                # perventing any new/more items to be added if there was no items remove
                if slot.removeItem(item, 1):
                    self.addItem(item, 1)
                    return True
        return False

    def calculateItemWeight(self, item):
        raise NotImplementedError()

    def calculateItemWorth(self, item):
        self._verifyArguments(item)

        # Calcuates the total worth for the item, regarding where it is on the "Creature"
        worth = 0
        for slot in self.container.values():
            # Verify a slot is a slot type
            if not isinstance(slot, Slot): continue
            # Checks if item in the misc or if equipped
            if item.slot_type == slot.type or slot.type == setting.MISC_SLOT:
                worth += slot.calculateItemWorth(item)
        return worth

    def calculateTotalWeight(self):
        raise NotImplementedError()

    def calculateTotalWorth(self) -> int:
        # Calcuates the total worth of all coin and items regarding where it is on the "Creature"
        worth = 0
        for slot in self.container.values():
            if not isinstance(slot, Slot): continue
            worth += slot.calculateTotalWorth()
        return worth



def main():
    import items
    a = OneHanded()
    b = OneHanded()
    c = TwoHanded()
    a1 = items.Bread()
    a.addItem(a1, 2)

    print(a==b)
    print(a is b)
    print(a.container==b.container)
    print(a.container is b.container)



    print('_'*20)
    print(a == c)
    print(a is c , "here")
    print(a.container==c.container)
    print(a.container is c.container)

    Inventory()


if __name__ == "__main__":
    main()
