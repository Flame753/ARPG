import items
from abc import ABC


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


class Creature(ABC):
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

        self.slot_list = list()

    def define_slots(self):
        for bodypart, slot in EQUIP_SLOTS.items():
            self.slot_list.extend(slot*self.__dict__.get(bodypart))

    def ensure_equipment_slots(self):
        if not hasattr(self, 'equipment_slots'):
            self.equipment_slots = {}

    def slots_exist(self, slot):
        return True if slot in self.slot_list else False

    def slot_available(self, slot):
        self.ensure_equipment_slots()
        # Checks if the slot doesn't exist
        if not self.slots_exist(slot): return False
        # Checks if an item is occupying the slot
        return False if self.equipment_slots.get(slot, None) else True

    def add_equipment(self, item, slot):
        self.ensure_equipment_slots()

        if self.slot_available(slot):
            self.equipment_slots[slot] = item
            return True
        return False

    def is_alive(self):
        return self.hp > 0
    
    def change_physical_body(self, **kwargs):
        for key in kwargs.keys():
            if not hasattr(self, key): return False
        self.__dict__.update(kwargs)
        return True

class Humonoid(Creature, items.Container):
    def __init__(self, heads=1, eyes=2, legs=2, hands=2, fingers=10, **kwargs):
        super().__init__(heads=heads, eyes=eyes, legs=legs, hands=hands, fingers=fingers, **kwargs)
        if type(self) == Humonoid:
            raise Exception('Do not instantiate Humonoid directly')

    def add_items(self, items):
        for item, amount in items.items():
            self.addItem(item, amount)

class Beast(Creature):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        if type(self) == Beast:
            raise Exception('Do not instantiate Beast directly')
        

if __name__ == '__main__':
    pass
