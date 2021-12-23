from abc import ABC


# Equipment Slots that are Exist
EQUIP_SLOT = ['EQUIP_SLOT_HEAD',
            'EQUIP_SLOT_NECK',
            'EQUIP_SLOT_TORSO',
            'EQUIP_SLOT_WAIST',
            'EQUIP_SLOT_LEGS',
            'EQUIP_SLOT_FEETS',
            'EQUIP_SLOT_MAIN_HAND',
            'EQUIP_SLOT_OFF_HAND',
            'EQUIP_SLOT_RING',
            'EQUIP_SLOT_TAIL',
            'EQUIP_SLOT_WINGS',]


class EquipSlot(ABC):
    def __init__(self):
        if type(self) == EquipSlot:
            raise Exception('Do not instantiate EquipSlot directly')
        self.slots = list()

    def ensure_equipment_slots(self):
        if not hasattr(self, 'equipment_slots'):
            self.equipment_slots = {}

    def slots_exist(self, slot):
        return True if slot in self.slots else False

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

    # def add_equipments(self, item, slots):
    #     if type(item) == item and type(slots) == list:
    #         for num, loc in enumerate(slots):
    #             print(loc)
    #             if loc in self.slots:
    #                 pass


    # def change_equipment(self, **kwargs):
    #     self.ensure_equipment_slots()

    #     # Changes current equipment out with new one
    #     for key, value in kwargs.items():
    #         if key in self.equimplment_slots:
    #             pass
    #         if value:
    #             # Returns Equipment back into bag
    #             self.bag.addItem(self.__dict__[key], 1)
    #     self.__dict__.update(kwargs)
    #     return True

class Creature(EquipSlot):
    def __init__(self, heads=1, eyes=2, body=1, legs=2, hands=2, fingers=10, tails=0, wings=0, **kwargs):
        if type(self) == Creature:
            raise Exception('Do not instantiate Creature directly')
        self.heads = heads
        self.eyes = eyes
        self.body = body
        self.legs = legs
        self.hands = hands
        self.fingers = fingers
        self.tails = tails
        self.wings = wings

    def is_alive(self):
        return self.hp > 0
    
    def change_physical_body(self, **kwargs):
        for key in kwargs.keys():
            if not hasattr(self, key): return False
        self.__dict__.update(kwargs)
        return True

class Humonoid(Creature):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        if type(self) == Humonoid:
            raise Exception('Do not instantiate Humonoid directly')

        self.slots = ['EQUIP_SLOT_HEAD',
                    'EQUIP_SLOT_NECK',
                    'EQUIP_SLOT_TORSO',
                    'EQUIP_SLOT_WAIST',
                    'EQUIP_SLOT_LEGS',
                    'EQUIP_SLOT_FEETS',
                    'EQUIP_SLOT_MAIN_HAND',
                    'EQUIP_SLOT_OFF_HAND',
                    'EQUIP_SLOT_RING']

class Beast(Creature):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        if type(self) == Beast:
            raise Exception('Do not instantiate Beast directly')
        
        self.slots = ['EQUIP_SLOT_HEAD',
            'EQUIP_SLOT_NECK',
            'EQUIP_SLOT_TORSO',
            'EQUIP_SLOT_WAIST',
            'EQUIP_SLOT_LEGS',
            'EQUIP_SLOT_FEETS',
            'EQUIP_SLOT_LEGS',
            'EQUIP_SLOT_FEETS', 
            'EQUIP_SLOT_TAIL']

if __name__ == '__main__':
    import items
    c = Creature()
    print(c.slots_exist('EQUIP_SLOT_TORSO'))
    c.add_equipment(items.HealingPotion(), 'EQUIP_SLOT_TORSO')
    print(c.equipment_slots)
    print(c.slot_available('EQUIP_SLOT_TORSO'))
    # c.addEquipment(items.Dagger(), ['EQUIP_SLOT_TAIL'])
