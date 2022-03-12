# Standard library imports 
from pprint import pprint
import unittest

# Local application imports
from context import entities
from entities import creatures
from entities import items
from entities import currency
from entities import slots



class TestCreature(unittest.TestCase):
    def setUp(self):
        self.dagger = items.Dagger()
        self.copper_coin = currency.CopperCoin()
        self.bread = items.Bread()

    def equipment_slot_helper(self, creature_obj, answer):
        self.assertDictEqual(creature_obj.equippable_slots.slots.get(slots.Head).container, answer) 
        self.assertDictEqual(creature_obj.equippable_slots.slots.get(slots.Body).container, answer) 
        self.assertDictEqual(creature_obj.equippable_slots.slots.get(slots.Legs).container, answer)
        self.assertDictEqual(creature_obj.equippable_slots.slots.get(slots.Boots).container, answer)
        self.assertDictEqual(creature_obj.equippable_slots.slots.get(slots.OneHanded).container, answer) 
        self.assertDictEqual(creature_obj.equippable_slots.slots.get(slots.TwoHanded).container, answer) 

    def test_class_initializer(self):
        creature_A = creatures.Creature()
        creature_B = creatures.Creature()

        self.assertFalse(creature_A is creature_B)
        self.assertFalse(creature_A.equippable_slots is creature_B.equippable_slots)

        self.assertEqual(creature_A.inventory, creature_B.inventory)
        self.assertFalse(creature_A.inventory is creature_B.inventory)

        self.assertEqual(creature_A.coin_pouch, creature_B.coin_pouch)
        self.assertFalse(creature_A.coin_pouch is creature_B.coin_pouch)

    def test_addItem(self):
        creature = creatures.Creature()

        creature.addItem(self.dagger)
        self.assertDictEqual(creature.inventory.container, 
                            {self.dagger: {'amount': 1}}) 

        creature.addItem(self.copper_coin, 2)
        self.assertDictEqual(creature.coin_pouch.container, 
                            {self.copper_coin: {'amount': 2}}) 

        creature.addItem(self.bread, 6)
        self.assertDictEqual(creature.inventory.container, 
                            {self.bread: {'amount': 6}, self.dagger: {'amount': 1}}) 

        creature.addItem(self.dagger, 3)
        self.assertDictEqual(creature.inventory.container, 
                            {self.bread: {'amount': 6}, self.dagger: {'amount': 4}}) 

    def test_removeItem(self):
        creature = creatures.Creature()

        # Testing when removing an item from a empty dict
        result = creature.removeItem(self.dagger)
        self.assertFalse(result)
 
        creature.addItem(self.dagger)
        creature.removeItem(self.dagger)
        self.assertDictEqual(creature.inventory.container, {}) 

        creature.addItem(self.copper_coin, 8)
        creature.removeItem(self.copper_coin, 3)
        self.assertDictEqual(creature.coin_pouch.container, 
                            {self.copper_coin: {'amount': 5}}) 

    def test_equip(self):
        creature = creatures.Creature()
        # Equipping dagger that is not in creature
        result = creature.equip(self.dagger)
        self.assertFalse(result)
        # Verifying that there is no container was added
        answer = {}
        self.equipment_slot_helper(creature, answer)

        result = creature.inventory.container
        self.assertDictEqual(result, answer) 

        result = creature.coin_pouch.container
        self.assertDictEqual(result, answer) 

        # Equipping non equipable item
        creature.addItem(self.copper_coin)
        result = creature.equip(self.copper_coin)
        self.assertFalse(result)
        # Verifying that there is no container was added
        answer = {self.copper_coin: {'amount': 1}}
        result = creature.coin_pouch.container
        self.assertDictEqual(result, answer) 

        answer = {}
        self.equipment_slot_helper(creature, answer)

        result = creature.inventory.container
        self.assertDictEqual(result, answer) 


        # Equipping a dagger 
        creature.addItem(self.dagger)
        result = creature.equip(self.dagger)
        self.assertTrue(result)
        
        answer = {self.dagger: {'amount': 1}}
        result = creature.inventory.container
        self.assertDictEqual(result, answer)

        answer = {self.dagger: {'amount': 1}}
        result = creature.equippable_slots.slots.get(slots.OneHanded).container
        self.assertDictEqual(result, answer) 

        # equipping a non equipable item
        creature.addItem(self.bread)
        result = creature.equip(self.bread)
        self.assertFalse(result)

    def test_unequip(self):
        creature = creatures.Creature()

        # Unequipping a item that doesn't exist
        result = creature.unequip(self.dagger)
        self.assertFalse(result)
        # Verifying that there is no container was added
        answer = {}
        self.equipment_slot_helper(creature, answer)

        result = creature.inventory.container
        self.assertDictEqual(result, answer)
    
        result = creature.coin_pouch.container
        self.assertDictEqual(result, answer) 

        creature.addItem(self.copper_coin)
        result = creature.unequip(self.copper_coin)
        self.assertFalse(result)
        # Verifying that there is no container was added
        answer = {}
        self.equipment_slot_helper(creature, answer)

        result = creature.inventory.container
        self.assertDictEqual(result, answer)

        answer = {self.copper_coin: {'amount': 1}}
        result = creature.coin_pouch.container
        self.assertDictEqual(result, answer) 
        # Preparing for next test case
        creature.removeItem(self.copper_coin)
        
        # Actually tesing the removal of a item
        creature.addItem(self.dagger)
        creature.equip(self.dagger)
        result = creature.unequip(self.dagger)
        self.assertTrue(result)
        answer = {}
        self.equipment_slot_helper(creature, answer)

        result = creature.coin_pouch.container
        self.assertDictEqual(result, answer)
         
        answer = {self.dagger: {'amount': 1}}
        result = creature.inventory.container
        self.assertDictEqual(result, answer)

    def test_calculateItemWorth(self):
        creature = creatures.Creature()
        copper_amount = 10
        bread_amount = 5
        dagger_amount = 5
        creature.addItem(self.copper_coin, copper_amount)
        creature.addItem(self.bread, bread_amount)
        creature.addItem(self.dagger, dagger_amount)
        creature.equip(self.dagger)

        result = creature.calculateItemWorth(self.copper_coin)
        self.assertEqual(result, copper_amount*self.copper_coin.worth)

        result = creature.calculateItemWorth(self.dagger)
        self.assertEqual(result, dagger_amount*self.dagger.worth)

        result = creature.calculateItemWorth(self.bread)
        self.assertEqual(result, bread_amount*self.bread.worth)

    def test_calculateTotalWorth(self):
        creature = creatures.Creature()
        copper_amount = 10
        bread_amount = 5
        dagger_amount = 5
        creature.addItem(self.copper_coin, copper_amount)
        creature.addItem(self.bread, bread_amount)
        creature.addItem(self.dagger, dagger_amount)
        creature.equip(self.dagger)

        result = creature.calculateTotalWorth()
        answer = (self.copper_coin.worth * copper_amount) + \
                (self.dagger.worth * dagger_amount) + \
                (self.bread.worth * bread_amount)
        self.assertEqual(result, answer)

    def test_typeError(self):
        creature = creatures.Creature()
        test_num = 2
        test_string = 'Test'
        test_list = [7]
        test_dict = {"s":2}
        test_tuple = (2, "2")

        test_case = [test_num, test_string, test_list, test_dict, test_tuple, [], {}, ()]
        for case in test_case:
            func = creature.addItem
            self.assertRaises(TypeError, func, case)
            self.assertRaises(TypeError, func, (self.dagger, case))
            func = creature.removeItem
            self.assertRaises(TypeError, func, case)
            self.assertRaises(TypeError, func, (self.dagger, case))
            func = creature.equip
            self.assertRaises(TypeError, func, case)
            func = creature.unequip
            self.assertRaises(TypeError, func, case)
            func = creature.calculateItemWorth
            self.assertRaises(TypeError, func, case)
            func = creature.calculateTotalWorth
            self.assertRaises(TypeError, func, case)

    def test_valueError(self):
        creature = creatures.Creature()
        test_case = -32

        func = creature.addItem
        self.assertRaises(TypeError, func, (self.dagger, test_case))
        func = creature.removeItem
        self.assertRaises(TypeError, func, (self.dagger, test_case))

    def test_EquippedItemRemovealError(self):
        creature = creatures.Creature()
        # Tesing after removing item from inventory item should not exist in equipment slot
        creature.addItem(self.dagger)
        creature.equip(self.dagger)
        self.assertRaises(creatures.EquippedItemRemovealError, creature.removeItem, self.dagger)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestCreature('test_addItem'))
    return suite


if __name__ == '__main__':
    unittest.main()
    # runner = unittest.TextTestRunner()
    # runner.run(suite())