# Standard library imports 
from pprint import pprint
import unittest

# Local application imports
# from context import arpg
# from arpg.entities import items
# from arpg.entities import slots

from context import entities
from entities import items
from entities import slots
from entities import setting


class TestSlot(unittest.TestCase):
    def setUp(self):
        self.dagger = items.Dagger()
        self.copper_coin = items.CopperCoin()
        self.bread = items.Bread()
    
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

        head_A.addItem(self.dagger)
        self.assertNotEqual(head_A, head_B)
        self.assertFalse(head_A is head_B)

        self.assertNotEqual(legs_A, body_A)
        self.assertFalse(legs_A is body_A)

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

    def test_removeitem(self):
        slot = slots.Slot()
        self.assertFalse(slot.removeItem(self.dagger))
        
        slot.addItem(self.dagger)
        self.assertFalse(slot.removeItem(self.dagger, 2))
        self.assertDictEqual(slot.container, {self.dagger: {'amount': 1}})

        self.assertTrue(slot.removeItem(self.dagger))
        self.assertDictEqual(slot.container, {})

    def test_calculateItemWorth(self):
        slot = slots.Slot()

        copper_amount = 10
        slot.addItem(self.copper_coin, copper_amount)
        self.assertEqual(slot.calculateItemWorth(self.copper_coin), copper_amount*self.copper_coin.worth)

        bread_amount = 5
        slot.addItem(self.bread, bread_amount)
        self.assertEqual(slot.calculateItemWorth(self.bread), bread_amount*self.bread.worth)

        dagger_amount = 5
        slot.addItem(self.dagger, dagger_amount)
        self.assertEqual(slot.calculateItemWorth(self.dagger), dagger_amount*self.dagger.worth)

    def test_calculateTotalWorth(self):
        slot = slots.Slot()

        self.assertEqual(slot.calculateTotalWorth(), 0)

        copper_amount = 10
        slot.addItem(self.copper_coin, copper_amount)
        answer = copper_amount*self.copper_coin.worth
        self.assertEqual(slot.calculateTotalWorth(), answer)

        bread_amount = 5
        slot.addItem(self.bread, bread_amount)
        answer = answer + (bread_amount * self.bread.worth)
        self.assertEqual(slot.calculateTotalWorth(), answer)

        dagger_amount = 5
        slot.addItem(self.dagger, dagger_amount)
        answer = answer + (dagger_amount * self.dagger.worth)
        self.assertEqual(slot.calculateTotalWorth(), answer)


class TestEquipmentSlots(unittest.TestCase):
    def setUp(self):
        self.dagger = items.Dagger()
        self.copper_coin = items.CopperCoin()
        self.bread = items.Bread()
        self.axe = items.Axe()

    def test_class_initializer(self):
        eq_slot_A = slots.EquipmentSlots()
        eq_slot_B = slots.EquipmentSlots()

        self.assertEqual(eq_slot_A.slots, eq_slot_B.slots)
        self.assertFalse(eq_slot_A.slots is eq_slot_B.slots)

        eq_slot_A.equip(self.dagger)
        self.assertNotEqual(eq_slot_A.slots, eq_slot_B.slots)
        self.assertFalse(eq_slot_A.slots is eq_slot_B.slots)
    
    def test_equip(self):
        eq_slot = slots.EquipmentSlots()

        self.assertTrue(eq_slot.equip(self.dagger))
        self.assertDictEqual(eq_slot.slots.get(setting.ONE_HANDED_SLOT).container, {self.dagger: {'amount': 1}})
        with self.assertRaises(slots.CapacityReachedError):
            eq_slot.equip(self.dagger)

        self.assertFalse(eq_slot.equip(self.bread))
        self.assertFalse(eq_slot.equip(self.copper_coin))

    def test_unequip(self):
        eq_slot = slots.EquipmentSlots()

        self.assertFalse(eq_slot.unequip(self.dagger))
        self.assertDictEqual(eq_slot.slots.get(setting.ONE_HANDED_SLOT).container, {})

        self.assertFalse(eq_slot.unequip(self.bread))
        self.assertFalse(eq_slot.unequip(self.copper_coin))

        eq_slot.equip(self.dagger)
        self.assertTrue(eq_slot.unequip(self.dagger))
        self.assertDictEqual(eq_slot.slots.get(setting.ONE_HANDED_SLOT).container, {})

    def test_isItemEquipped(self):
        eq_slot = slots.EquipmentSlots()

        self.assertFalse(eq_slot.isItemEquipped(self.dagger))
        self.assertFalse(eq_slot.isItemEquipped(self.bread))
        self.assertFalse(eq_slot.isItemEquipped(self.copper_coin))

        eq_slot.equip(self.dagger)
        self.assertTrue(eq_slot.isItemEquipped(self.dagger))

    def test_locateSlotByItem(self):
        eq_slot = slots.EquipmentSlots()
        # self.assertEqual(eq_slot.locateSlotByItem(), slots.Head())
        # self.assertEqual(eq_slot.locateSlotByItem(), slots.Body())
        # self.assertEqual(eq_slot.locateSlotByItem(), slots.Legs())
        # self.assertEqual(eq_slot.locateSlotByItem(), slots.Boots())
        self.assertEqual(eq_slot.locateSlotByItem(self.dagger), slots.OneHanded())
        self.assertEqual(eq_slot.locateSlotByItem(self.axe), slots.TwoHanded())


if __name__ == '__main__':
    unittest.main()
