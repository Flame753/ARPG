from creatures import Creature
from pprint import pprint
import unittest
import items


class TestCreatures(unittest.TestCase):
    def setUp(self):
        self.dagger = items.Dagger()
        self.copper_coin = items.CopperCoin()
        self.bread = items.Bread()

    def test_class_initializer(self):
        creature_A = Creature()
        creature_B = Creature()

        self.assertEqual(creature_A, creature_B)
        self.assertFalse(creature_A is creature_B)

        self.assertEqual(creature_A.head, creature_B.head)
        self.assertFalse(creature_A.head is creature_B.head)

        self.assertEqual(creature_A.body, creature_B.body)
        self.assertFalse(creature_A.body is creature_B.body)

        self.assertEqual(creature_A.legs, creature_B.legs)
        self.assertFalse(creature_A.legs is creature_B.legs)

        self.assertEqual(creature_A.one_handed, creature_B.one_handed)
        self.assertFalse(creature_A.one_handed is creature_B.one_handed)

        self.assertEqual(creature_A.two_handed, creature_B.two_handed)
        self.assertFalse(creature_A.one_handed is creature_B.two_handed)

        self.assertEqual(creature_A.inventory, creature_B.inventory)
        self.assertFalse(creature_A.inventory is creature_B.inventory)

        self.assertEqual(creature_A.coin, creature_B.coin)
        self.assertFalse(creature_A.coin is creature_B.coin)

    def test_addItem(self):
        creature = Creature()

        creature.addItem(self.dagger)
        answer = {self.dagger: {'amount': 1}}
        self.assertDictEqual(creature.inventory.container, answer) 

        creature.addItem(self.copper_coin, 2)
        answer = {self.copper_coin: {'amount': 2}}
        self.assertDictEqual(creature.coin.container, answer)

        creature.addItem(self.bread, 6)
        answer = {self.bread: {'amount': 6}, self.dagger: {'amount': 1}}
        self.assertDictEqual(creature.inventory.container, answer)

        creature.addItem(self.dagger, 3)
        answer = {self.bread: {'amount': 6}, self.dagger: {'amount': 4}}
        self.assertDictEqual(creature.inventory.container, answer)  

    def test_removeItem(self):
        creature = Creature()

        # Testing when removing an item from a empty dict
        result = creature.removeItem(self.dagger)
        self.assertFalse(result)
 
        creature.addItem(self.dagger)
        creature.removeItem(self.dagger)
        answer = {}
        self.assertDictEqual(creature.inventory.container, answer)

        creature.addItem(self.copper_coin, 8)
        creature.removeItem(self.copper_coin, 3)
        answer = {self.copper_coin: {'amount': 5}}
        self.assertDictEqual(creature.coin.container, answer)

    def test_equip(self):
        creature = Creature()
        # Equipping dagger that is not in inventory
        result = creature.equip(self.dagger)
        self.assertFalse(result)
        # Verifying that there is no items was added
        answer = {}
        self.assertDictEqual(creature.head.container, answer)
        self.assertDictEqual(creature.body.container, answer)
        self.assertDictEqual(creature.legs.container, answer)
        self.assertDictEqual(creature.one_handed.container, answer)
        self.assertDictEqual(creature.two_handed.container, answer)
        self.assertDictEqual(creature.inventory.container, answer)
        self.assertDictEqual(creature.coin.container, answer)

        # Equipping non equipable item
        creature.addItem(self.copper_coin)
        result = creature.equip(self.copper_coin)
        self.assertFalse(result)
        # Verifying that there is no items was added
        answer = {self.copper_coin: {'amount': 1}}
        self.assertDictEqual(creature.coin.container, answer)
        answer = {}
        self.assertDictEqual(creature.head.container, answer)
        self.assertDictEqual(creature.body.container, answer)
        self.assertDictEqual(creature.legs.container, answer)
        self.assertDictEqual(creature.one_handed.container, answer)
        self.assertDictEqual(creature.two_handed.container, answer)
        self.assertDictEqual(creature.inventory.container, answer)

        # Equipping a dagger 
        creature.addItem(self.dagger)
        result = creature.equip(self.dagger)
        self.assertTrue(result)
        answer = {}
        self.assertDictEqual(creature.inventory.container, answer)
        answer = {self.dagger: {'amount': 1}}
        self.assertDictEqual(creature.one_handed.container, answer)

    def test_unequip(self):
        creature = Creature()

        # Unequipping a item that doesn't exist
        result = creature.unequip(self.dagger)
        self.assertFalse(result)
        # Verifying that there is no items was added
        answer = {}
        self.assertDictEqual(creature.head.container, answer)
        self.assertDictEqual(creature.body.container, answer)
        self.assertDictEqual(creature.legs.container, answer)
        self.assertDictEqual(creature.one_handed.container, answer)
        self.assertDictEqual(creature.two_handed.container, answer)
        self.assertDictEqual(creature.inventory.container, answer)
        self.assertDictEqual(creature.coin.container, answer)

        creature.addItem(self.copper_coin)
        result = creature.unequip(self.copper_coin)
        self.assertFalse(result)
        # Verifying that there is no items was added
        answer = {}
        self.assertDictEqual(creature.head.container, answer)
        self.assertDictEqual(creature.body.container, answer)
        self.assertDictEqual(creature.legs.container, answer)
        self.assertDictEqual(creature.one_handed.container, answer)
        self.assertDictEqual(creature.two_handed.container, answer)
        self.assertDictEqual(creature.inventory.container, answer)
        answer = {self.copper_coin: {'amount': 1}}
        self.assertDictEqual(creature.coin.container, answer)
        # Preparing for next test case
        creature.removeItem(self.copper_coin)
        
        # Actually tesing the removal of a item
        creature.addItem(self.dagger)
        creature.equip(self.dagger)
        result = creature.unequip(self.dagger)
        self.assertTrue(result)
        answer = {}
        self.assertDictEqual(creature.head.container, answer)
        self.assertDictEqual(creature.body.container, answer)
        self.assertDictEqual(creature.legs.container, answer)
        self.assertDictEqual(creature.one_handed.container, answer)
        self.assertDictEqual(creature.two_handed.container, answer)
        self.assertDictEqual(creature.coin.container, answer)
        answer = {self.dagger: {'amount': 1}}
        self.assertDictEqual(creature.inventory.container, answer)

    def test_calculateItemWorth(self):
        creature = Creature()
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
        creature = Creature()
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
        creature = Creature()
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
        creature = Creature()
        test_case = -32

        func = creature.addItem
        self.assertRaises(TypeError, func, (self.dagger, test_case))
        func = creature.removeItem
        self.assertRaises(TypeError, func, (self.dagger, test_case))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestCreatures('test_addItem'))
    return suite

if __name__ == '__main__':
    unittest.main()
    # runner = unittest.TextTestRunner()
    # runner.run(suite())