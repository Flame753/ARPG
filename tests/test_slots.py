# Standard library imports 
from pprint import pprint
import unittest

# Local application imports
from context import items
from context import slots


class TestSlot(unittest.TestCase):
    def setUp(self):
        self.dagger = items.Dagger()
        self.copper_coin = items.CopperCoin()
        self.bread = items.Bread()

    def test_addItem(self):
        slot = slots.Slot()

        self.assertDictEqual(slot.container, {})
        slot.addItem(self.dagger)
        self.assertDictEqual(slot.container, {self.dagger: {'amount': 1}})
        slot.addItem(self.copper_coin, 6)
        self.assertDictEqual(slot.container, {self.dagger: {'amount': 1},
                                            self.copper_coin: {'amount': 6}})

    def test_isCapacityReached(self):
        slot = slots.Slot()

        # testing when item_limit is None
        self.assertFalse(slot._isCapacityReached())

        slot.item_limit = 0
        self.assertTrue(slot._isCapacityReached())

        slot.item_limit = 2
        self.assertFalse(slot._isCapacityReached())

        amount = 2
        slot.addItem(self.dagger, amount)
        self.assertTrue(slot._isCapacityReached(amount))

    def test_item_limit(self):
        slot = slots.Slot()
        slot.item_limit = 2

        # Passing the limit in a singe time
        with self.assertRaises(slots.CapacityReachedError):
            slot.addItem(self.dagger, 3)
        self.assertDictEqual(slot.container, {})

        slot.addItem(self.dagger, 2)
        with self.assertRaises(slots.CapacityReachedError):
            slot.addItem(self.dagger, 1)
            slot.addItem(self.copper_coin, 3)

    def test_isCorrectSlot(self):
        pass

    def test_removeitem(self):
        slot = slots.Slot()
        self.assertFalse(slot.removeItem(self.dagger))
        
        slot.addItem(self.dagger)
        self.assertFalse(slot.removeItem(self.dagger, 2))
        self.assertDictEqual(slot.container, {self.dagger: {'amount': 1}})

        self.assertTrue(slot.removeItem(self.dagger))
        self.assertDictEqual(slot.container, {})

    def test_calculateItemWorth(self):
        pass

    def test_caluclateTotalWorth(self):
        pass


if __name__ == '__main__':
    unittest.main()
    # runner = unittest.TextTestRunner()
    # runner.run(suite())
