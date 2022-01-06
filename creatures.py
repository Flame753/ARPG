from items import BaseItem, Inventory, Container


# Equipment Slots that are Exist
EQUIP_SLOTS = {'heads': ['EQUIP_SLOT_HEAD',
                        'EQUIP_SLOT_FOREHEAD',
                        'EQUIP_SLOT_NECK',],
            'eyes': [],
            'upper_body': ['EQUIP_SLOT_CHEST',
                        'EQUIP_SLOT_WAIST',],
            'legs': ['EQUIP_SLOT_LEGS',
                    'EQUIP_SLOT_FEETS',],
            'hands': ['EQUIP_SLOT_TWO_HAND',
                            'EQUIP_SLOT_MAIN_HAND',
                            'EQUIP_SLOT_OFF_HAND',],
            'fingers': ['EQUIP_SLOT_RING'],
            'tails': ['EQUIP_SLOT_TAIL'],
            'wings': ['EQUIP_SLOT_WINGS']}


class Creature(Inventory):
    def __init__(self, heads=0, eyes=0, upper_body=0, legs=0, hands=0, fingers=0, tails=0, wings=0, **kwargs):
        if type(self) == Creature:
            raise Exception('Do not instantiate Creature directly')
        self.heads = heads
        self.eyes = eyes
        self.upper_body = upper_body
        self.legs = legs
        self.hands = hands
        self.fingers = fingers
        self.tails = tails
        self.wings = wings

    # Methods that deal with Equipment Slots
    def define_slots(self) -> dict:
        pair_of = ['eyes', 'legs', 'hands', 'wings']
        default_slot = {}
        for bodypart, slots in EQUIP_SLOTS.items():
            for slot in slots:
                if bodypart in pair_of:
                    amount_of_parts = self.__dict__.get(bodypart)
                    default_slot.update({slot: (amount_of_parts//2)})   
                else:
                    default_slot.update({slot: self.__dict__.get(bodypart)})
        return default_slot

    def ensure_equipment_slots(self):
        if not hasattr(self, 'equipment_slots'):
            equipment_slots = {}
            slots = self.define_slots()
            for slot, amount in slots.items():
                equipment_slots[slot] = {'amount': amount}
                equipment_slots[slot]['items'] = []
            self.equipment_slots = equipment_slots
    
    def proper_slot(self, item: BaseItem, slot: str):
        pass

    def add_item_to_slot(self, item: BaseItem, slot: str) -> bool:
        self.ensure_equipment_slots()
        slot = self.equipment_slots.get(slot, None)

        # Slot doesn't exist
        if not slot: return False
        items = slot['items']
        amount = slot['amount']

        # Slot fully occupying 
        if len(items) == amount: return False
        items.append(item)
        return True

    def remove_item_from_slot(self, item: BaseItem, slot: str) -> bool:
        self.ensure_equipment_slots()
        slot = self.equipment_slots.get(slot, None)

        # Slot doesn't exist
        if not slot: return False
        items = slot['items']
        if item in items:
            items.remove(item)
            return True
        return False

    # Methods that deal with the Creature's inventory 
    # including any methods that are form the Container class
    def add_item(self, item, amount=0, container=None):
        if isinstance(container, Container):
            container.ensure_inventory()
            if item in container.inventory:
                container.inventory[item]['amount'] += amount
            else:
                container.inventory[item] = {'amount': amount}
        else:
            self.ensure_inventory()
            if item in self.inventory:
                self.inventory[item]['amount'] += amount
            else:
                self.inventory[item] = {'amount': amount}

    def remove_item(self, item, amount=0, container=None):
        if isinstance(container, Container):
            container.ensure_inventory()
            if item in container.inventory:
                if container.inventory[item]['amount'] >= amount:
                    container.inventory[item]['amount'] -= amount
                    if container.inventory[item]['amount'] == 0:
                        del(container.inventory[item])
                    return True
            return False
        else:
            self.ensure_inventory()
            if item in self.inventory:
                if self.inventory[item]['amount'] >= amount:
                    self.inventory[item]['amount'] -= amount
                    if self.inventory[item]['amount'] == 0:
                        del(self.inventory[item])
                    return True
            return False

    def calculate_total_weight(self):
        self.ensure_inventory()

        weight = 0
        for item, data in self.inventory.items():
            weight += item.weight * data['amount']
            if isinstance(item, Container):
                for i, data in item.inventory.items():
                    weight += i.weight * data['amount']
        return weight

    def calculate_total_worth(self):
        self.ensure_inventory()

        worth = 0
        for item, data in self.inventory.items():
            worth += item.worth * data['amount']
            if isinstance(item, Container):
                for i, data in item.inventory.items():
                    worth += i.worth * data['amount']
        return worth
    
    def find_item(self, item:BaseItem) -> list[BaseItem]:
        # Finds a specific item in the creature's inventory or in a container that 
        # might be in the inventory and then returns that container with the item.
        self.ensure_inventory()
        if self.inventory.get(item, None): return self.inventory

        # Finds the first Container Object that has the item
        for item in self.inventory:
            if isinstance(item, Container):
                item.ensure_inventory()
                if item.inventory.get(item, None): return item.inventory
        return None

    def equip_item(self, container, item, slot):
        self.ensure_equipment_slots()
        if not container: return False

        if self.add_item_to_slot(item, slot): 
            self.remove_item(item, 1, container)
            self.add_item(item, 1)
        return True

    def unquip_item(self, container, item, slot):
        self.ensure_equipment_slots()

        if self.remove_item_from_slot(item, slot): 
            self.remove_item(item, 1)
            self.add_item(item, 1, container)
            return True
        return False

    # Methods that deal with physical form
    def change_physical_body(self, **kwargs):
        for key in kwargs.keys():
            if not hasattr(self, key): return False
        self.__dict__.update(kwargs)
        return True

    def is_alive(self):
        return self.hp > 0
    

class Humonoid(Creature):
    def __init__(self, heads=1, eyes=2, upper_body=1, legs=2, hands=2, fingers=10, **kwargs):
        super().__init__(heads=heads, eyes=eyes, upper_body=upper_body, legs=legs, hands=hands, fingers=fingers, **kwargs)
        # if type(self) == Humonoid:
        #     raise Exception('Do not instantiate Humonoid directly')


class Beast(Creature):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        if type(self) == Beast:
            raise Exception('Do not instantiate Beast directly')
        

if __name__ == '__main__':
    import items
    h = Humonoid()
    d = items.Dagger()
    b = items.Backpack()
    starting_equipment = {items.Rock(): 3,
                    d: 1,
                    items.Bread(): 2,
                    b: 1}
    for k, v in starting_equipment.items():
        # h.ensure_inventory()
        h.add_item(k, v)
    # print(h.inventory)
    # h.ensure_equipment_slots()
    # b.ensure_inventory()
    # print(h.inventory, h.equipment_slots)
    print(h.equip_item(h, d, 'EQUIP_SLOT_HEAD'))
    # print(h.inventory, h.equipment_slots)
    print(h.unquip_item(b, d, 'EQUIP_SLOT_HEAD'))
    # print(h.inventory, h.equipment_slots)
    # print("bag:", b.inventory)
    print(h.equip_item(b, d, 'EQUIP_SLOT_HEAD'))
    print(h.equipment_slots)
    # print(h.inventory, h.equipment_slots)
    # print("bag:", b.inventory)
    # print(h.add_item(h.inventory, items.Backpack(), 1))
    # print(h.inventory)
