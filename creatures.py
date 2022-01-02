from items import BaseItem, Inventory, Container


# Equipment Slots that are Exist
EQUIP_SLOTS = {'heads': ['EQUIP_SLOT_HEAD',
                    'EQUIP_SLOT_NECK',],
            'eyes': [],
            'body': ['EQUIP_SLOT_TORSO',
                    'EQUIP_SLOT_WAIST',],
            'legs': ['EQUIP_SLOT_LEGS',
                    'EQUIP_SLOT_FEETS',],
            'hands': ['EQUIP_SLOT_MAIN_HAND',
                    'EQUIP_SLOT_OFF_HAND',],
            'fingers': ['EQUIP_SLOT_RING'],
            'tails': ['EQUIP_SLOT_TAIL'],
            'wings': ['EQUIP_SLOT_WINGS']}

def GET_EQUIP_SLOTS():
    slots = list()
    for slot in EQUIP_SLOTS.values():
        slots.extend(slot)
    return slots


class Creature(Inventory):
    def __init__(self, heads=0, eyes=0, body=0, legs=0, hands=0, fingers=0, tails=0, wings=0, **kwargs):
        if type(self) == Creature:
            raise Exception('Do not instantiate Creature directly')
        self.heads = heads
        self.eyes = eyes//2
        self.body = body
        self.legs = legs//2
        self.hands = hands//2
        self.fingers = fingers//max(1, hands)
        self.tails = tails
        self.wings = wings

        self.ensure_slot_list()
        self.ensure_inventory()
        self.ensure_equipment_slots()

    # Methods that deal with Equipment Slots
    def define_slots(self):
        self.ensure_slot_list()
        for bodypart, slot in EQUIP_SLOTS.items():
            self.slot_list.extend(slot*self.__dict__.get(bodypart))

    def ensure_slot_list(self):
        if not hasattr(self, 'equipment_slots'):
            self.slot_list = list()

    def ensure_equipment_slots(self):
        if not hasattr(self, 'equipment_slots'):
            equipment_slots = {}
            self.define_slots()
            self.equipment_slots = equipment_slots.fromkeys(self.slot_list, None)
            
    def slot_exist(self, slot):
        self.ensure_slot_list()
        return True if slot in self.slot_list else False

    def slot_available(self, slot):
        self.ensure_equipment_slots()
        # Checks if the slot doesn't exist
        if not self.slot_exist(slot): return False
        # Checks if an item is occupying the slot
        return False if self.equipment_slots.get(slot, None) else True
    
    def proper_slot(self, item, slot):
        pass

    def add_item_to_slot(self, item, slot):
        # Adds item into equipment slot
        self.ensure_equipment_slots()
        if self.slot_available(slot):
            self.equipment_slots[slot] = item
            return True
        return False
    
    def remove_item_from_slot(self, slot):
        # Removes item from equipment slot
        self.ensure_equipment_slots()
        if self.slot_exist(slot):
            self.equipment_slots[slot] = None
            return True
        return False

    # Methods that deal with the Creature's inventory 
    # including any methods that are form the Container class
    @staticmethod
    def add_item(inventory, item, amount=0):
        if not isinstance(item, Inventory): pass
        print(inventory,)
        if item in inventory:
            inventory[item]['amount'] += amount
        else:
            inventory[item] = {'amount': amount}

    @staticmethod
    def remove_item(inventory, item, amount=0):
        if not isinstance(item, Inventory): pass
        if item in inventory:
            if inventory[item]['amount'] >= amount:
                inventory[item]['amount'] -= amount
                if inventory[item]['amount'] == 0:
                    del(inventory[item])
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

    def equip_item(self, storage_locker, item, slot):
        self.ensure_equipment_slots()
        if not storage_locker: return False

        if self.add_item_to_slot(item, slot): 
            self.remove_item(storage_locker, item, 1)
            self.add_item(self.inventory, item, 1)
        return True

    def unquip_item(self, storage_locker, item, slot):
        self.ensure_equipment_slots()

        if self.remove_item_from_slot(slot): 
            self.remove_item(self.inventory, item, 1)
            self.add_item(storage_locker, item, 1)
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
    def __init__(self, heads=1, eyes=2, legs=2, hands=2, fingers=10, **kwargs):
        super().__init__(heads=heads, eyes=eyes, legs=legs, hands=hands, fingers=fingers, **kwargs)
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
        h.add_item(h.inventory, k, v)
    # print(h.inventory)
    # h.ensure_equipment_slots()
    # b.ensure_inventory()
    print(h.inventory, h.equipment_slots)
    print(h.equip_item(h.inventory, d, 'EQUIP_SLOT_HEAD'))
    print(h.inventory, h.equipment_slots)
    print(h.unquip_item(b.inventory, d, 'EQUIP_SLOT_HEAD'))
    print(h.inventory, h.equipment_slots)
    # print(h.add_item(h.inventory, items.Backpack(), 1))
    # print(h.inventory)
