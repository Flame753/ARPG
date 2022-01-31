import unittest
from creatures import Creature
from pprint import pprint


class TestCreatures(unittest.TestCase):
    def setUp(self):
        import items

        self.dagger = items.Dagger()
        self.copper_coin = items.CopperCoin()
        self.bread = items.Bread()

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
        pprint(creature)

    def test_equip(self):
        pass

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