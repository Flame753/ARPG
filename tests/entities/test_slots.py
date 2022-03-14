# Standard library imports 
from pprint import pprint
import unittest

# Local application imports
from context import entities
from entities import items
from entities import currency
from entities import slots



class TestSlot(unittest.TestCase):
    def setUp(self):
        self.dagger = items.Dagger()
        self.copper_coin = currency.CopperCoin()
        self.bread = items.Bread()

        self.slot = slots.Slot('slot', 20)
        self.slot._ensure_inventory()
    
    def test_class_initializer(self):
        head_A = slots.Head()
        body_A = slots.Body()
        legs_A = slots.Legs()

        head_B = slots.Head()
        body_B = slots.Body()

        self.assertEqual(head_A, head_B)
        self.assertFalse(head_A is head_B)

        self.assertEqual(body_A, body_B)
        self.assertFalse(body_A is body_B)

        head_A.add_item(self.dagger)
        self.assertFalse(head_A is head_B)
        self.assertTrue(hasattr(head_A, 'inventory'))
        self.assertFalse(hasattr(head_B, 'inventory'))

        self.assertNotEqual(legs_A, body_A)
        self.assertFalse(legs_A is body_A)

    def test_add_item(self):
        self.assertDictEqual(self.slot.inventory, {})
        self.slot.add_item(self.dagger)
        self.assertDictEqual(self.slot.inventory, {self.dagger: {'amount': 1}})
        self.slot.add_item(self.copper_coin, 6)
        self.assertDictEqual(self.slot.inventory, {self.dagger: {'amount': 1},
                                            self.copper_coin: {'amount': 6}})

    def test_is_capacity_reached(self):
        # testing when item_limit is None
        self.assertFalse(self.slot._is_capacity_reached())

        self.slot.item_limit = 0
        self.assertTrue(self.slot._is_capacity_reached())

        self.slot.item_limit = 2
        self.assertFalse(self.slot._is_capacity_reached())

        amount = 2
        self.slot.add_item(self.dagger, amount)
        self.assertTrue(self.slot._is_capacity_reached(amount))

    def test_item_limit(self):
        self.slot.item_limit = 2

        # Passing the limit in a singe time
        with self.assertRaises(slots.CapacityReachedError):
            self.slot.add_item(self.dagger, 3)
        self.assertDictEqual(self.slot.inventory, {})

        self.slot.add_item(self.dagger, 2)
        with self.assertRaises(slots.CapacityReachedError):
            self.slot.add_item(self.dagger, 1)
            self.slot.add_item(self.copper_coin, 3)

    def test_remove_item(self):
        self.assertFalse(self.slot.remove_item(self.dagger))
        
        self.slot.add_item(self.dagger)
        self.assertFalse(self.slot.remove_item(self.dagger, 2))
        self.assertDictEqual(self.slot.inventory, {self.dagger: {'amount': 1}})

        self.assertTrue(self.slot.remove_item(self.dagger))
        self.assertDictEqual(self.slot.inventory, {})

    def test_calculate_item_worth(self):
        copper_amount = 10
        self.slot.add_item(self.copper_coin, copper_amount)
        self.assertEqual(self.slot.calculate_item_worth(self.copper_coin), copper_amount*self.copper_coin.worth)

        bread_amount = 5
        self.slot.add_item(self.bread, bread_amount)
        self.assertEqual(self.slot.calculate_item_worth(self.bread), bread_amount*self.bread.worth)

        dagger_amount = 5
        self.slot.add_item(self.dagger, dagger_amount)
        self.assertEqual(self.slot.calculate_item_worth(self.dagger), dagger_amount*self.dagger.worth)

    def test_calculate_total_worth(self):
        self.assertEqual(self.slot.calculate_total_worth(), 0)

        copper_amount = 10
        self.slot.add_item(self.copper_coin, copper_amount)
        answer = copper_amount*self.copper_coin.worth
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
        self.coin_pouch = slots.Coins()
        self.copper = currency.CopperCoin()
        self.silver = currency.SilverCoin()
        self.gold = currency.GoldCoin()
        self.platinum = currency.PlatinumCoin()

        self.coin_pouch.add_item(self.copper)
        self.coin_pouch.add_item(self.silver)
        self.coin_pouch.add_item(self.gold)
        self.coin_pouch.add_item(self.platinum)

    def test_have_coin(self):
        self.assertTrue(self.coin_pouch.have_coin(self.copper))
        self.assertTrue(self.coin_pouch.have_coin(self.silver))
        self.assertTrue(self.coin_pouch.have_coin(self.gold))
        self.assertTrue(self.coin_pouch.have_coin(self.platinum))
        
        self.coin_pouch.add_item(self.copper)
        self.assertTrue(self.coin_pouch.have_coin(self.copper, 2))

        self.coin_pouch.add_item(self.silver, 3)
        self.assertTrue(self.coin_pouch.have_coin(self.silver, 4))
        self.assertFalse(self.coin_pouch.have_coin(self.silver, 5))

        self.coin_pouch.add_item(self.gold, 6)
        self.assertTrue(self.coin_pouch.have_coin(self.gold, 7))
        self.coin_pouch.remove_item(self.gold, 7)
        self.assertFalse(self.coin_pouch.have_coin(self.gold))

        with self.assertRaises(ValueError):
            self.coin_pouch.have_coin(self.platinum, 0)
            self.coin_pouch.have_coin(self.platinum, -2)

    def test_order(self):
        pass

    def test_find_largest_coin(self):
        self.assertEqual(self.coin_pouch.find_largest_coin(), self.platinum)


class TestEquipmentSlots(unittest.TestCase):
    def setUp(self):
        self.dagger = items.Dagger()
        self.copper_coin = currency.CopperCoin()
        self.bread = items.Bread()
        self.axe = items.Axe()

        self.eq_slot = slots.EquipmentSlots()

    def test_class_initializer(self):
        eq_slot_A = slots.EquipmentSlots()
        eq_slot_B = slots.EquipmentSlots()

        self.assertEqual(eq_slot_A.slots, eq_slot_B.slots)
        self.assertFalse(eq_slot_A.slots is eq_slot_B.slots)

        eq_slot_A.equip(self.dagger)

        self.assertFalse(eq_slot_A.slots is eq_slot_B.slots)
        self.assertTrue(hasattr(eq_slot_A.slots.get(slots.OneHanded), 'inventory'))
        self.assertFalse(hasattr(eq_slot_B.slots.get(slots.OneHanded), 'inventory'))

        self.assertEqual(eq_slot_A.slots.get(slots.OneHanded).name, "One Handed Slot")
    
    def test_equip(self):
        self.assertTrue(self.eq_slot.equip(self.dagger))
        self.assertDictEqual(self.eq_slot.slots.get(slots.OneHanded).inventory, {self.dagger: {'amount': 1}})
        with self.assertRaises(slots.CapacityReachedError):
            self.eq_slot.equip(self.dagger)

        self.assertFalse(self.eq_slot.equip(self.bread))
        self.assertFalse(self.eq_slot.equip(self.copper_coin))

    def test_unequip(self):
        self.assertFalse(self.eq_slot.unequip(self.dagger))
        self.assertDictEqual(self.eq_slot.slots.get(slots.OneHanded).inventory, {})

        self.assertFalse(self.eq_slot.unequip(self.bread))
        self.assertFalse(self.eq_slot.unequip(self.copper_coin))

        self.eq_slot.equip(self.dagger)
        self.assertTrue(self.eq_slot.unequip(self.dagger))
        self.assertDictEqual(self.eq_slot.slots.get(slots.OneHanded).inventory, {})

    def test_is_item_equipped(self):
        self.assertFalse(self.eq_slot.is_item_equipped(self.dagger))
        self.assertFalse(self.eq_slot.is_item_equipped(self.bread))
        self.assertFalse(self.eq_slot.is_item_equipped(self.copper_coin))

        self.eq_slot.equip(self.dagger)
        self.assertTrue(self.eq_slot.is_item_equipped(self.dagger))

    def test_locate_slot_by_item(self):
        # self.assertEqual(eq_slot.locate_slot_by_item(), slots.Head())
        # self.assertEqual(eq_slot.locate_slot_by_item(), slots.Body())
        # self.assertEqual(eq_slot.locate_slot_by_item(), slots.Legs())
        # self.assertEqual(eq_slot.locate_slot_by_item(), slots.Boots())
        self.assertEqual(self.eq_slot.locate_slot_by_item(self.dagger), slots.OneHanded())
        self.assertEqual(self.eq_slot.locate_slot_by_item(self.axe), slots.TwoHanded())


if __name__ == '__main__':
    unittest.main()
