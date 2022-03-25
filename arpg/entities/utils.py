# Standard library imports  
from abc import ABC


class Container(ABC):
    def _ensure_inventory(self) -> None:
        if not hasattr(self, 'inventory'):
            self.inventory = dict()

    def add_item(self, item, amount: int = 0) -> None:
        self._ensure_inventory()

        if amount < 0: raise ValueError

        if item in self.inventory:
            self.inventory[item]['amount'] += amount
        else:
            self.inventory[item] = {'amount': amount}

    def remove_item(self, item, amount: int = 0) -> bool:
        self._ensure_inventory()

        if amount < 0: raise ValueError

        if item in self.inventory:
            if self.inventory[item]['amount'] >= amount:
                self.inventory[item]['amount'] -= amount
                if self.inventory[item]['amount'] == 0:
                    del(self.inventory[item])
                return True
        return False

    def calculate_item_weight(self, item) -> int:
        self._ensure_inventory()

        if item in self.inventory:
            return item.weight * self.inventory[item]['amount']
        return 0

    def calculate_item_worth(self, item)  -> int:
        self._ensure_inventory()

        if item in self.inventory:
            return item.worth * self.inventory[item]['amount']
        return 0

    def calculate_total_weight(self) -> int:
        self._ensure_inventory()

        weight = 0
        for item, data in self.inventory.items():
            weight += item.weight * data['amount']
        return weight

    def calculate_total_worth(self) -> int:
        self._ensure_inventory()

        worth = 0
        for item, data in self.inventory.items():
            worth += item.worth * data['amount']
        return worth