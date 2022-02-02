import unittest
from creatures import Creature
from pprint import pprint


class TestCreatures(unittest.TestCase):
    def setUp(self):
        import items

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
        self.assertDictEqual(creature.inventory.container, answer)
        answer = {}
        self.assertDictEqual(creature.one_handed.container, answer)

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
        pass

    def test_calculateItemWorth(self):
        pass

    def test_calculateTotalWorth(self):
        pass

    def test_typeError(self):
        pass

    def test_valueError(self):
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestCreatures('test_addItem'))
    return suite

if __name__ == '__main__':
    unittest.main()
    # runner = unittest.TextTestRunner()
    # runner.run(suite())