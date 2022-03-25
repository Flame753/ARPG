# Standard library imports 
from pprint import pprint
import unittest

# Local application imports
from context import entities
from entities import currency
from entities import items
from entities import slots



class TestSlot(unittest.TestCase):
    def setUp(self):
        self.dagger = items.Dagger()
        self.bread = items.Bread()
        self.copper = currency.CopperCoin()

        self.slot = slots.Slot('Any Slot', items.BaseItem)
    
    def test_class_initializer(self):
        Primary = slots.Slot('Any Slot', items.BaseItem)
        Secondary = slots.Slot('Any Slot', items.BaseItem)
        
        self.assertIsNot(Primary, Secondary)

        self.assertTrue(hasattr(Primary, 'name'))
        self.assertTrue(hasattr(Primary, 'items_allowed'))
        self.assertFalse(hasattr(Primary, 'inventory'))

        Primary._ensure_inventory()
        self.assertTrue(hasattr(Primary, 'inventory'))

    def test_add_item(self):
        self.assertFalse(hasattr(self.slot, 'inventory'))

        self.slot.add_item(self.dagger)
        self.assertTrue(hasattr(self.slot, 'inventory'))
        self.assertDictEqual(self.slot.inventory, {self.dagger: {'amount': 1}})

        self.slot.add_item(self.copper, 6)
        self.assertDictEqual(self.slot.inventory, {self.dagger: {'amount': 1},
                                                    self.copper: {'amount': 6}})

        with self.assertRaises(ValueError):
            self.slot.add_item(self.bread, -2)
        self.assertDictEqual(self.slot.inventory, {self.dagger: {'amount': 1},
                                                    self.copper: {'amount': 6}})

    def test_remove_item(self):
        self.assertFalse(hasattr(self.slot, 'inventory'))

        # Removing an item out of non-existencing inventory
        self.assertFalse(self.slot.remove_item(self.dagger))
        # The remove_item method should created an inventory
        self.assertTrue(hasattr(self.slot, 'inventory'))

        self.slot.add_item(self.dagger)
        self.assertFalse(self.slot.remove_item(self.dagger, 2))
        self.assertDictEqual(self.slot.inventory, {self.dagger: {'amount': 1}})

        with self.assertRaises(ValueError):
            self.slot.remove_item(self.dagger, -2)
        self.assertDictEqual(self.slot.inventory, {self.dagger: {'amount': 1}})

        self.assertTrue(self.slot.remove_item(self.dagger))
        self.assertDictEqual(self.slot.inventory, {})

    def test_calculate_item_worth(self):
        self.assertFalse(hasattr(self.slot, 'inventory'))

        # Caluclating the total worth of a item
        self.assertEqual(self.slot.calculate_item_worth(self.copper), 0)
        self.assertTrue(hasattr(self.slot, 'inventory'))

        copper_amount = 10
        self.slot.add_item(self.copper, copper_amount)
        self.assertEqual(self.slot.calculate_item_worth(self.copper), copper_amount*self.copper.worth)

        bread_amount = 5
        self.slot.add_item(self.bread, bread_amount)
        self.assertEqual(self.slot.calculate_item_worth(self.bread), bread_amount*self.bread.worth)

        dagger_amount = 5
        self.slot.add_item(self.dagger, dagger_amount)
        self.assertEqual(self.slot.calculate_item_worth(self.dagger), dagger_amount*self.dagger.worth)

    def test_calculate_total_worth(self):
        self.assertFalse(hasattr(self.slot, 'inventory'))
        self.assertEqual(self.slot.calculate_total_worth(), 0)

        copper_amount = 10
        self.slot.add_item(self.copper, copper_amount)
        answer = copper_amount*self.copper.worth
        self.assertEqual(self.slot.calculate_total_worth(), answer)

        bread_amount = 5
        self.slot.add_item(self.bread, bread_amount)
        answer = answer + (bread_amount * self.bread.worth)
        self.assertEqual(self.slot.calculate_total_worth(), answer)

        dagger_amount = 5
        self.slot.add_item(self.dagger, dagger_amount)
        answer = answer + (dagger_amount * self.dagger.worth)
        self.assertEqual(self.slot.calculate_total_worth(), answer)


class TestCoinSlot(unittest.TestCase):
    def setUp(self):
        self.dagger = items.Dagger()
        self.bread = items.Bread()
        self.copper = currency.CopperCoin()
        self.silver = currency.SilverCoin()
        self.gold = currency.GoldCoin()
        self.platinum = currency.PlatinumCoin()

        self.coin_slot = slots.Coins()
        self.coin_slot.add_item(self.copper)
        self.coin_slot.add_item(self.silver)
        self.coin_slot.add_item(self.gold)
        self.coin_slot.add_item(self.platinum)

    def test_add_item(self):
        with self.assertRaises(slots.ItemFilterError):
            self.coin_slot.add_item(self.dagger)

        with self.assertRaises(slots.ItemFilterError):
            self.coin_slot.add_item(self.bread)

        self.coin_slot.add_item(self.copper)
        self.assertDictEqual(self.coin_slot.inventory, {self.copper: {'amount': 2},
                                                        self.silver: {'amount': 1},
                                                        self.gold: {'amount': 1},
                                                        self.platinum: {'amount': 1}})

    def test_remove_item(self):
        self.assertFalse(self.coin_slot.remove_item(self.dagger))
        self.assertFalse(self.coin_slot.remove_item(self.bread))

        self.coin_slot.add_item(self.copper)
        self.assertFalse(self.coin_slot.remove_item(self.copper, 6))
        self.assertTrue(self.coin_slot.remove_item(self.copper))
        self.assertDictEqual(self.coin_slot.inventory, {self.copper: {'amount': 1},
                                                        self.silver: {'amount': 1},
                                                        self.gold: {'amount': 1},
                                                        self.platinum: {'amount': 1}})

    def test_have_coin(self):
        self.assertTrue(self.coin_slot.have_coin(self.copper))
        self.assertTrue(self.coin_slot.have_coin(self.silver))
        self.assertTrue(self.coin_slot.have_coin(self.gold))
        self.assertTrue(self.coin_slot.have_coin(self.platinum))
        
        self.coin_slot.add_item(self.copper)
        self.assertTrue(self.coin_slot.have_coin(self.copper, 2))

        self.coin_slot.add_item(self.silver, 3)
        self.assertTrue(self.coin_slot.have_coin(self.silver, 4))
        self.assertFalse(self.coin_slot.have_coin(self.silver, 5))

        self.coin_slot.add_item(self.gold, 6)
        self.assertTrue(self.coin_slot.have_coin(self.gold, 7))
        self.coin_slot.remove_item(self.gold, 7)
        self.assertFalse(self.coin_slot.have_coin(self.gold))

        with self.assertRaises(ValueError):
            self.coin_slot.have_coin(self.platinum, 0)
            self.coin_slot.have_coin(self.platinum, -2)

    def test_order(self):
        coins = self.coin_slot.order()
        self.assertListEqual(coins, [self.copper, self.silver, self.gold, self.platinum])

        self.coin_slot.remove_item(self.gold)
        coins = self.coin_slot.order()
        self.assertListEqual(coins, [self.copper, self.silver, self.platinum])
    
    def test_find_largest(self):
        self.assertEqual(self.coin_slot.find_largest_coin(), self.platinum)
        
        self.coin_slot.remove_item(self.platinum)
        self.coin_slot.remove_item(self.gold)
        self.assertEqual(self.coin_slot.find_largest_coin(), self.silver)
        

class TestEquipmentSlots(unittest.TestCase):
    def setUp(self):
        self.dagger = items.Dagger()
        self.axe = items.Axe()
        self.bread = items.Bread()
        self.copper = currency.CopperCoin()
        
        self.eq_slot = slots.EquippableSlots("Equipment Slot", items.BaseItem, 1)

    def test_is_capacity_reached(self):
        self.assertFalse(self.eq_slot._capacity_reached())
        self.eq_slot.inventory[self.dagger] = {'amount': 1}
        self.assertTrue(self.eq_slot._capacity_reached())

    def test_CapacityReachedError(self):
        self.eq_slot.add_item(self.dagger)
        with self.assertRaises(slots.CapacityReachedError):
            self.eq_slot.add_item(self.dagger)
        
        self.eq_slot.remove_item(self.dagger)
        with self.assertRaises(slots.CapacityReachedError):
            self.eq_slot.add_item(self.dagger, 2)

    def test_special_case(self):
        special_slot = slots.EquippableSlots("Special Equipment Slot", items.BaseItem, 0)
        self.assertTrue(special_slot._capacity_reached())
        with self.assertRaises(slots.CapacityReachedError):
            special_slot.add_item(self.dagger)


if __name__ == '__main__':
    unittest.main()
