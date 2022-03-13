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

    def test_add_item(self):
        creature = creatures.Creature()

        creature.add_item(self.dagger)
        self.assertDictEqual(creature.inventory.container, 
                            {self.dagger: {'amount': 1}}) 

        creature.add_item(self.copper_coin, 2)
        self.assertDictEqual(creature.coin_pouch.container, 
                            {self.copper_coin: {'amount': 2}}) 

        creature.add_item(self.bread, 6)
        self.assertDictEqual(creature.inventory.container, 
                            {self.bread: {'amount': 6}, self.dagger: {'amount': 1}}) 

        creature.add_item(self.dagger, 3)
        self.assertDictEqual(creature.inventory.container, 
                            {self.bread: {'amount': 6}, self.dagger: {'amount': 4}}) 

    def test_remove_item(self):
        creature = creatures.Creature()

        # Testing when removing an item from a empty dict
        result = creature.remove_item(self.dagger)
        self.assertFalse(result)
 
        creature.add_item(self.dagger)
        creature.remove_item(self.dagger)
        self.assertDictEqual(creature.inventory.container, {}) 

        creature.add_item(self.copper_coin, 8)
        creature.remove_item(self.copper_coin, 3)
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
        creature.add_item(self.copper_coin)
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
        creature.add_item(self.dagger)
        result = creature.equip(self.dagger)
        self.assertTrue(result)
        
        answer = {self.dagger: {'amount': 1}}
        result = creature.inventory.container
        self.assertDictEqual(result, answer)

        answer = {self.dagger: {'amount': 1}}
        result = creature.equippable_slots.slots.get(slots.OneHanded).container
        self.assertDictEqual(result, answer) 

        # equipping a non equipable item
        creature.add_item(self.bread)
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

        creature.add_item(self.copper_coin)
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
        creature.remove_item(self.copper_coin)
        
        # Actually tesing the removal of a item
        creature.add_item(self.dagger)
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

    def test_calculate_item_worth(self):
        creature = creatures.Creature()
        copper_amount = 10
        bread_amount = 5
        dagger_amount = 5
        creature.add_item(self.copper_coin, copper_amount)
        creature.add_item(self.bread, bread_amount)
        creature.add_item(self.dagger, dagger_amount)
        creature.equip(self.dagger)

        result = creature.calculate_item_worth(self.copper_coin)
        self.assertEqual(result, copper_amount*self.copper_coin.worth)

        result = creature.calculate_item_worth(self.dagger)
        self.assertEqual(result, dagger_amount*self.dagger.worth)

        result = creature.calculate_item_worth(self.bread)
        self.assertEqual(result, bread_amount*self.bread.worth)

    def test_calculate_total_worth(self):
        creature = creatures.Creature()
        copper_amount = 10
        bread_amount = 5
        dagger_amount = 5
        creature.add_item(self.copper_coin, copper_amount)
        creature.add_item(self.bread, bread_amount)
        creature.add_item(self.dagger, dagger_amount)
        creature.equip(self.dagger)

        result = creature.calculate_total_worth()
        answer = (self.copper_coin.worth * copper_amount) + \
                (self.dagger.worth * dagger_amount) + \
                (self.bread.worth * bread_amount)
        self.assertEqual(result, answer)

    def test_type_error(self):
        creature = creatures.Creature()
        test_num = 2
        test_string = 'Test'
        test_list = [7]
        test_dict = {"s":2}
        test_tuple = (2, "2")

        test_case = [test_num, test_string, test_list, test_dict, test_tuple, [], {}, ()]
        for case in test_case:
            func = creature.add_item
            self.assertRaises(TypeError, func, case)
            self.assertRaises(TypeError, func, (self.dagger, case))
            func = creature.remove_item
            self.assertRaises(TypeError, func, case)
            self.assertRaises(TypeError, func, (self.dagger, case))
            func = creature.equip
            self.assertRaises(TypeError, func, case)
            func = creature.unequip
            self.assertRaises(TypeError, func, case)
            func = creature.calculate_item_worth
            self.assertRaises(TypeError, func, case)
            func = creature.calculate_total_worth
            self.assertRaises(TypeError, func, case)

    def test_value_error(self):
        creature = creatures.Creature()
        test_case = -32

        func = creature.add_item
        self.assertRaises(TypeError, func, (self.dagger, test_case))
        func = creature.remove_item
        self.assertRaises(TypeError, func, (self.dagger, test_case))

    def test_EquippedItemRemovealError(self):
        creature = creatures.Creature()
        # Tesing after removing item from inventory item should not exist in equipment slot
        creature.add_item(self.dagger)
        creature.equip(self.dagger)
        self.assertRaises(creatures.EquippedItemRemovealError, creature.remove_item, self.dagger)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestCreature('test_addItem'))
    return suite


if __name__ == '__main__':
    unittest.main()
    # runner = unittest.TextTestRunner()
    # runner.run(suite())