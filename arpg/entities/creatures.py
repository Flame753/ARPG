# Standard library imports 
from typing import Optional
from dataclasses import dataclass, field
from pprint import pprint

# Local application imports
from entities import items
from entities import currency
from entities import slots



# Constant Variables
ITEMS = "items"
CONSUMABLES = "consumables"
COINS = "coins"
WEAPONS = "weapons"
ARMOR = "armor"

HEAD = "head"
BODY = "body"
LEGS = "legs"
BOOTS = "boots"
ONE_HANDED = "one_handed"
TWO_HANDED = "two_handed"



class NonEquippableError(Exception):
    """Exception raised for non-equippable item was used."""
    
    def __init__(self, message="Non-Equippable Items are not supported!"):
        self.message = message
        super().__init__(self.message)



# @dataclass() 
class Creature():
    def __init__(self):
        self.equipment = {ITEMS: slots.Items(),
                        CONSUMABLES: slots.Consumables(),
                        COINS: slots.Coins(),
                        WEAPONS: slots.Weapons(),
                        ARMOR: slots.Armor()}

        self.armor = {HEAD: slots.Head(), 
                    BODY: slots.Body(), 
                    LEGS: slots.Legs(), 
                    BOOTS: slots.Boots(),
                    ONE_HANDED: slots.OneHanded(), 
                    TWO_HANDED: slots.TwoHanded()}

        self.hp = 100
        self.max_hp = 100

    def _verify_arguments(self, item: items.BaseItem=None, amount: int=None) -> None:
        # Verifys if Arguments are enter correctly 
        if item:
            if not isinstance(item, items.BaseItem):
                raise TypeError(f'The item argument requires to be a items.BaseItem Object, not a {type(item)}!')
        if amount:
            if not type(amount) == int:
                raise TypeError(f'The amount argurment requires to be a intger, not a {type(amount)}!')
            if amount < 0:
                raise ValueError("The amount argurment can't be an negative real number!")
        if type(item) in [list, dict, tuple] or type(amount) in [list, dict, tuple]:
            raise TypeError(f"Arguments can't be a empty List, Dictionary or Tuple")

    # Methods that deal with any items
    def find_equipment_slot(self, item: items.BaseItem) -> slots.Slot:

        type_of_items = [COINS, CONSUMABLES, WEAPONS, ARMOR, ITEMS]

        for slot in type_of_items:
            if isinstance(item, self.equipment.get(slot).items_allowed):
                return self.equipment.get(slot)

    def add_item(self, item: items.BaseItem, amount: int=1) -> None:
        self._verify_arguments(item, amount)
        slot = self.find_equipment_slot(item)
        slot.add_item(item, amount)

    def remove_item(self, item: items.BaseItem, amount: int=1) -> bool:
        self._verify_arguments(item, amount)
        slot = self.find_equipment_slot(item)
        return slot.remove_item(item, amount)

    # Methods that deal with equipping items
    def find_armor_slot(self, item: items.BaseItem) -> Optional[slots.Slot]:
        type_of_items = [HEAD, BODY, LEGS, BOOTS, ONE_HANDED, TWO_HANDED]

        for slot in type_of_items:
            if isinstance(item, self.armor.get(slot).items_allowed):
                return self.armor.get(slot)

    def equip(self, item: items.BaseItem) -> bool:
        self._verify_arguments(item)

        armor_slot = self.find_armor_slot(item)
        equipment_slot = self.find_equipment_slot(item)

        if not armor_slot: raise NonEquippableError("Unable to Equip a Non-Equippable Items!") # Preventing any non-equippable items
        
        armor_slot._ensure_inventory()
        equipment_slot._ensure_inventory()

        if item not in equipment_slot.inventory: return False # No items to equip
        try:
            armor_slot.add_item(item)
        except slots.CapacityReachedError:
            return False
        return equipment_slot.remove_item(item)

    def item_already_equipped(self, item: items.BaseItem) -> bool:
        slot = self.find_armor_slot(item)
        if not slot: raise NonEquippableError() # Preventing any non-equippable items
        slot._ensure_inventory()
        return item in slot.inventory

    def unequip(self, item: items.BaseItem) -> bool:
        self._verify_arguments(item)
        armor_slot = self.find_armor_slot(item)
        equipment_slot = self.find_equipment_slot(item)

        if not armor_slot: raise NonEquippableError("Unable to Unequip a Non-Equippable Items!") # Preventing any non-equippable items
        
        armor_slot._ensure_inventory()
        equipment_slot._ensure_inventory()

        if item not in armor_slot.inventory: return False  # Nothing to unequipped

        equipment_slot.add_item(item)
        return armor_slot.remove_item(item)

    # Caluclations
    def calculate_item_worth(self, item: items.BaseItem) -> int:
        self._verify_arguments(item)
        armor_slot = self.find_armor_slot(item)
        equipment_slot = self.find_equipment_slot(item)
        if armor_slot:
            return equipment_slot.calculate_item_worth(item) + armor_slot.calculate_item_worth(item)
        else:
            return equipment_slot.calculate_item_worth(item)

    def calculate_total_worth(self) -> int:
        armor_slot_worth = 0
        equipment_slot_worth = 0

        for slot in self.armor.values():
            armor_slot_worth += slot.calculate_total_worth()

        for slot in self.equipment.values():
            equipment_slot_worth += slot.calculate_total_worth()

        return armor_slot_worth + equipment_slot_worth

    def is_alive(self) -> bool:
        return self.hp > 0
