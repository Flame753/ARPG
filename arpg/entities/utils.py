# Standard library imports  
from abc import ABC


class Container(ABC):
    def _ensure_inventory(self) -> None:
        if not hasattr(self, '_inventory'):
            self._inventory = dict()

    def get_inventory(self):
        self._ensure_inventory()
        return self._inventory

    def add_item(self, item, amount: int = 0) -> None:
        self._ensure_inventory()

        if amount < 0: raise ValueError

        if item in self._inventory:
            self._inventory[item]['amount'] += amount
        else:
            self._inventory[item] = {'amount': amount}

    def remove_item(self, item, amount: int = 0) -> bool:
        self._ensure_inventory()

        if amount < 0: raise ValueError

        if item in self._inventory:
            if self._inventory[item]['amount'] >= amount:
                self._inventory[item]['amount'] -= amount
                if self._inventory[item]['amount'] == 0:
                    del(self._inventory[item])
                return True
        return False

    def calculate_item_weight(self, item) -> int:
        self._ensure_inventory()

        if item in self._inventory:
            return item.weight * self._inventory[item]['amount']
        return 0

    def calculate_item_worth(self, item)  -> int:
        self._ensure_inventory()

        if item in self._inventory:
            return item.worth * self._inventory[item]['amount']
        return 0

    def calculate_total_weight(self) -> int:
        self._ensure_inventory()

        weight = 0
        for item, data in self._inventory.items():
            weight += item.weight * data['amount']
        return weight

    def calculate_total_worth(self) -> int:
        self._ensure_inventory()

        worth = 0
        for item, data in self._inventory.items():
            worth += item.worth * data['amount']
        return worth