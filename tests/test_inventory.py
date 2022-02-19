# Standard library imports 
from pprint import pprint
import unittest

# Local application imports
from context import items
from context import slots
from context import setting


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.dagger = items.Dagger()
        self.copper_coin = items.CopperCoin()
        self.bread = items.Bread()

    def test_class_initializer(self):
        inventory_A = slots.Inventory()
        inventory_B = slots.Inventory()

        result_A = inventory_A.container.get(setting.HEAD_SLOT).container
        result_B = inventory_B.container.get(setting.HEAD_SLOT).container
        self.assertEqual(result_A, result_B)
        self.assertFalse(result_A is result_B)

        result_A = inventory_A.container.get(setting.BODY_SLOT).container
        result_B = inventory_B.container.get(setting.BODY_SLOT).container
        self.assertEqual(result_A, result_B)
        self.assertFalse(result_A is result_B)

        result_A = inventory_A.container.get(setting.LEGS_SLOT).container
        result_B = inventory_B.container.get(setting.LEGS_SLOT).container
        self.assertEqual(result_A, result_B)
        self.assertFalse(result_A is result_B)

        result_A = inventory_A.container.get(setting.ONE_HANDED_SLOT).container
        result_B = inventory_B.container.get(setting.ONE_HANDED_SLOT).container
        self.assertEqual(result_A, result_B)
        self.assertFalse(result_A is result_B)

        result_A = inventory_A.container.get(setting.TWO_HANDED_SLOT).container
        result_B = inventory_B.container.get(setting.TWO_HANDED_SLOT).container
        self.assertEqual(result_A, result_B)
        self.assertFalse(result_A is result_B)

        result_A = inventory_A.container.get(setting.MISC_SLOT).container
        result_B = inventory_B.container.get(setting.MISC_SLOT).container
        self.assertEqual(result_A, result_B)
        self.assertFalse(result_A is result_B)

        result_A = inventory_A.container.get(setting.COIN_SLOT).container
        result_B = inventory_B.container.get(setting.COIN_SLOT).container
        self.assertEqual(result_A, result_B)
        self.assertFalse(result_A is result_B)

    
    def test_addItem(self):
        inventory = slots.Inventory()

        inventory.addItem(self.dagger)
        result = inventory.container.get(setting.MISC_SLOT).container
        answer = {self.dagger: {'amount': 1}}
        self.assertDictEqual(result, answer) 

        inventory.addItem(self.copper_coin, 2)
        result = inventory.container.get(setting.COIN_SLOT).container
        answer = {self.copper_coin: {'amount': 2}}
        self.assertDictEqual(result, answer) 

        inventory.addItem(self.bread, 6)
        result = inventory.container.get(setting.MISC_SLOT).container
        answer = {self.bread: {'amount': 6}, self.dagger: {'amount': 1}}
        self.assertDictEqual(result, answer) 

        inventory.addItem(self.dagger, 3)
        result = inventory.container.get(setting.MISC_SLOT).container
        answer = {self.bread: {'amount': 6}, self.dagger: {'amount': 4}}
        self.assertDictEqual(result, answer) 

    def test_removeItem(self):
        inventory = slots.Inventory()

        # Testing when removing an item from a empty dict
        result = inventory.removeItem(self.dagger)
        self.assertFalse(result)
 
        inventory.addItem(self.dagger)
        inventory.removeItem(self.dagger)
        result = inventory.container.get(setting.MISC_SLOT).container
        answer = {}
        self.assertDictEqual(result, answer) 

        inventory.addItem(self.copper_coin, 8)
        inventory.removeItem(self.copper_coin, 3)
        result = inventory.container.get(setting.COIN_SLOT).container
        answer = {self.copper_coin: {'amount': 5}}
        self.assertDictEqual(result, answer) 

    def test_equip(self):
        inventory = slots.Inventory()
        # Equipping dagger that is not in inventory
        result = inventory.equip(self.dagger)
        self.assertFalse(result)
        # Verifying that there is no items was added
        answer = {}
        result = inventory.container.get(setting.HEAD_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.BODY_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.LEGS_SLOT).container
        self.assertDictEqual(result, answer)

        result = inventory.container.get(setting.ONE_HANDED_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.TWO_HANDED_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.MISC_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.COIN_SLOT).container
        self.assertDictEqual(result, answer) 

        # Equipping non equipable item
        inventory.addItem(self.copper_coin)
        result = inventory.equip(self.copper_coin)
        self.assertFalse(result)
        # Verifying that there is no items was added
        answer = {self.copper_coin: {'amount': 1}}
        result = inventory.container.get(setting.COIN_SLOT).container
        self.assertDictEqual(result, answer) 

        answer = {}
        result = inventory.container.get(setting.HEAD_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.BODY_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.LEGS_SLOT).container
        self.assertDictEqual(result, answer)

        result = inventory.container.get(setting.ONE_HANDED_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.TWO_HANDED_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.MISC_SLOT).container
        self.assertDictEqual(result, answer) 


        # Equipping a dagger 
        inventory.addItem(self.dagger)
        result = inventory.equip(self.dagger)
        self.assertTrue(result)
        answer = {}
        result = inventory.container.get(setting.MISC_SLOT).container
        self.assertDictEqual(result, answer)

        answer = {self.dagger: {'amount': 1}}
        result = inventory.container.get(setting.ONE_HANDED_SLOT).container
        self.assertDictEqual(result, answer) 

    def test_unequip(self):
        inventory = slots.Inventory()

        # Unequipping a item that doesn't exist
        result = inventory.unequip(self.dagger)
        self.assertFalse(result)
        # Verifying that there is no items was added
        answer = {}
        result = inventory.container.get(setting.HEAD_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.BODY_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.LEGS_SLOT).container
        self.assertDictEqual(result, answer)

        result = inventory.container.get(setting.ONE_HANDED_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.TWO_HANDED_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.MISC_SLOT).container
        self.assertDictEqual(result, answer)
    
        result = inventory.container.get(setting.COIN_SLOT).container
        self.assertDictEqual(result, answer) 

        inventory.addItem(self.copper_coin)
        result = inventory.unequip(self.copper_coin)
        self.assertFalse(result)
        # Verifying that there is no items was added
        answer = {}
        result = inventory.container.get(setting.HEAD_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.BODY_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.LEGS_SLOT).container
        self.assertDictEqual(result, answer)

        result = inventory.container.get(setting.ONE_HANDED_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.TWO_HANDED_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.MISC_SLOT).container
        self.assertDictEqual(result, answer)

        answer = {self.copper_coin: {'amount': 1}}
        result = inventory.container.get(setting.COIN_SLOT).container
        self.assertDictEqual(result, answer) 
        # Preparing for next test case
        inventory.removeItem(self.copper_coin)
        
        # Actually tesing the removal of a item
        inventory.addItem(self.dagger)
        inventory.equip(self.dagger)
        result = inventory.unequip(self.dagger)
        self.assertTrue(result)
        answer = {}
        result = inventory.container.get(setting.HEAD_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.BODY_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.LEGS_SLOT).container
        self.assertDictEqual(result, answer)

        result = inventory.container.get(setting.ONE_HANDED_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.TWO_HANDED_SLOT).container
        self.assertDictEqual(result, answer) 

        result = inventory.container.get(setting.COIN_SLOT).container
        self.assertDictEqual(result, answer)
         
        answer = {self.dagger: {'amount': 1}}
        result = inventory.container.get(setting.MISC_SLOT).container
        self.assertDictEqual(result, answer)

    def test_calculateItemWorth(self):
        inventory = slots.Inventory()
        copper_amount = 10
        bread_amount = 5
        dagger_amount = 5
        inventory.addItem(self.copper_coin, copper_amount)
        inventory.addItem(self.bread, bread_amount)
        inventory.addItem(self.dagger, dagger_amount)
        inventory.equip(self.dagger)

        result = inventory.calculateItemWorth(self.copper_coin)
        self.assertEqual(result, copper_amount*self.copper_coin.worth)

        result = inventory.calculateItemWorth(self.dagger)
        self.assertEqual(result, dagger_amount*self.dagger.worth)

        result = inventory.calculateItemWorth(self.bread)
        self.assertEqual(result, bread_amount*self.bread.worth)

    def test_calculateTotalWorth(self):
        inventory = slots.Inventory()
        copper_amount = 10
        bread_amount = 5
        dagger_amount = 5
        inventory.addItem(self.copper_coin, copper_amount)
        inventory.addItem(self.bread, bread_amount)
        inventory.addItem(self.dagger, dagger_amount)
        inventory.equip(self.dagger)

        result = inventory.calculateTotalWorth()
        answer = (self.copper_coin.worth * copper_amount) + \
                (self.dagger.worth * dagger_amount) + \
                (self.bread.worth * bread_amount)
        self.assertEqual(result, answer)

    def test_typeError(self):
        inventory = slots.Inventory()
        test_num = 2
        test_string = 'Test'
        test_list = [7]
        test_dict = {"s":2}
        test_tuple = (2, "2")

        test_case = [test_num, test_string, test_list, test_dict, test_tuple, [], {}, ()]
        for case in test_case:
            func = inventory.addItem
            self.assertRaises(TypeError, func, case)
            self.assertRaises(TypeError, func, (self.dagger, case))
            func = inventory.removeItem
            self.assertRaises(TypeError, func, case)
            self.assertRaises(TypeError, func, (self.dagger, case))
            func = inventory.equip
            self.assertRaises(TypeError, func, case)
            func = inventory.unequip
            self.assertRaises(TypeError, func, case)
            func = inventory.calculateItemWorth
            self.assertRaises(TypeError, func, case)
            func = inventory.calculateTotalWorth
            self.assertRaises(TypeError, func, case)

    def test_valueError(self):
        inventory = slots.Inventory()
        test_case = -32

        func = inventory.addItem
        self.assertRaises(TypeError, func, (self.dagger, test_case))
        func = inventory.removeItem
        self.assertRaises(TypeError, func, (self.dagger, test_case))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestInventory('test_addItem'))
    return suite

if __name__ == '__main__':
    unittest.main()
    # runner = unittest.TextTestRunner()
    # runner.run(suite())