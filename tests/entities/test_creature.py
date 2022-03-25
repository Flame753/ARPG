# Standard library imports 
from pprint import pprint
import unittest

# Local application imports
from context import entities
from entities import creatures
from entities import currency
from entities import items
from entities import slots



class TestCreature(unittest.TestCase):
    def setUp(self):
        self.dagger = items.Dagger()
        self.copper_coin = currency.CopperCoin()
        self.bread = items.Bread()

        self.creature = creatures.Creature()

    def test_class_initializer(self):
        creature_A = creatures.Creature()
        creature_B = creatures.Creature()

        self.assertFalse(creature_A is creature_B)
        self.assertIsNot(creature_A.equipment, creature_B.equipment)

        self.assertEqual(creature_A.equipment.get(creatures.WEAPONS), 
                        creature_B.equipment.get(creatures.WEAPONS))
        self.assertIsNot(creature_A.equipment.get(creatures.WEAPONS), 
                        creature_B.equipment.get(creatures.WEAPONS))

        self.assertEqual(creature_A.equipment.get(creatures.COINS), 
                        creature_B.equipment.get(creatures.COINS))
        self.assertIsNot(creature_A.equipment.get(creatures.COINS), 
                        creature_B.equipment.get(creatures.COINS))

    def test_add_item(self):
        self.creature.add_item(self.dagger)
        self.assertDictEqual(self.creature.equipment.get(creatures.WEAPONS).inventory, 
                            {self.dagger: {'amount': 1}}) 

        self.creature.add_item(self.copper_coin, 2)
        self.assertDictEqual(self.creature.equipment.get(creatures.COINS).inventory, 
                            {self.copper_coin: {'amount': 2}}) 

        self.creature.add_item(self.bread, 6)
        self.assertDictEqual(self.creature.equipment.get(creatures.CONSUMABLES).inventory, 
                            {self.bread: {'amount': 6}}) 

        self.creature.add_item(self.dagger, 3)
        self.assertDictEqual(self.creature.equipment.get(creatures.WEAPONS).inventory, 
                            {self.dagger: {'amount': 4}}) 

    def test_remove_item(self):
        # Testing when removing an item from a empty dict
        self.assertFalse(self.creature.remove_item(self.dagger))
 
        self.creature.add_item(self.dagger)
        self.assertTrue(self.creature.remove_item(self.dagger))
        self.assertDictEqual(self.creature.equipment.get(creatures.WEAPONS).inventory, {}) 

        self.creature.add_item(self.copper_coin, 8)
        self.assertTrue(self.creature.remove_item(self.copper_coin, 3))
        self.assertDictEqual(self.creature.equipment.get(creatures.COINS).inventory, 
                            {self.copper_coin: {'amount': 5}}) 

    def test_find_equipment_slot(self):
        self.assertEqual(self.creature.find_equipment_slot(self.copper_coin), slots.Coins())
        self.assertEqual(self.creature.find_equipment_slot(self.bread), slots.Consumables())
        self.assertEqual(self.creature.find_equipment_slot(self.dagger), slots.Weapons())

    def test_find_armor_slot(self):
        self.assertEqual(self.creature.find_armor_slot(self.dagger), slots.OneHanded())

    def test_equip_with_empty_inventory(self):
        self.assertFalse(self.creature.equip(self.dagger))

        self.assertDictEqual(self.creature.armor.get(creatures.ONE_HANDED).inventory, {}) 

    def test_equip_item(self):
        self.creature.add_item(self.dagger)
        self.assertDictEqual(self.creature.equipment.get(creatures.WEAPONS).inventory, {self.dagger: {'amount': 1}})
        self.assertTrue(self.creature.equip(self.dagger))
        self.assertDictEqual(self.creature.armor.get(creatures.ONE_HANDED).inventory, {self.dagger: {'amount': 1}})
        self.assertDictEqual(self.creature.equipment.get(creatures.WEAPONS).inventory, {})

    def test_equip_non_eqippable_item(self):
        self.creature.add_item(self.copper_coin)
        with self.assertRaises(creatures.NonEquippableError):
            self.creature.equip(self.copper_coin)

        self.creature.add_item(self.bread)
        with self.assertRaises(creatures.NonEquippableError):
            self.creature.equip(self.bread)

    def test_equip_reached_capacity(self):
        self.creature.add_item(self.dagger, 2)
        self.creature.equip(self.dagger)
        self.assertFalse(self.creature.equip(self.dagger))

        self.assertDictEqual(self.creature.armor.get(creatures.ONE_HANDED).inventory, {self.dagger: {'amount': 1}})
        self.assertDictEqual(self.creature.equipment.get(creatures.WEAPONS).inventory, {self.dagger: {'amount': 1}})

    def test_item_already_equipped(self):
        self.assertFalse(self.creature.item_already_equipped(self.dagger))

        with self.assertRaises(creatures.NonEquippableError):
            self.assertFalse(self.creature.item_already_equipped(self.copper_coin))
        with self.assertRaises(creatures.NonEquippableError):
            self.assertFalse(self.creature.item_already_equipped(self.bread))

        self.creature.add_item(self.dagger)
        self.creature.equip(self.dagger)
        self.assertTrue(self.creature.item_already_equipped(self.dagger))

    def test_unequip_with_empty_inventory(self):
        self.assertFalse(self.creature.unequip(self.dagger))

        self.assertDictEqual(self.creature.armor.get(creatures.ONE_HANDED).inventory, {})
        self.assertDictEqual(self.creature.equipment.get(creatures.WEAPONS).inventory, {})

    def test_unequip_non_eqippable_item(self):
        self.creature.add_item(self.copper_coin)
        with self.assertRaises(creatures.NonEquippableError):
            self.creature.unequip(self.copper_coin)

        self.creature.add_item(self.bread)
        with self.assertRaises(creatures.NonEquippableError):
            self.creature.unequip(self.bread)

        # Verifying that there is no inventory was added
        self.assertDictEqual(self.creature.equipment.get(creatures.CONSUMABLES).inventory, {self.bread: {'amount': 1}})
        self.assertDictEqual(self.creature.equipment.get(creatures.COINS).inventory, {self.copper_coin: {'amount': 1}})   

    def test_unequip(self):
        # Actually tesing the removal of a item
        self.creature.add_item(self.dagger)
        self.creature.equip(self.dagger)

        self.assertDictEqual(self.creature.armor.get(creatures.ONE_HANDED).inventory, {self.dagger: {'amount': 1}})
        self.assertDictEqual(self.creature.equipment.get(creatures.WEAPONS).inventory, {})

        self.assertTrue(self.creature.unequip(self.dagger))

        self.assertDictEqual(self.creature.armor.get(creatures.ONE_HANDED).inventory, {})
        self.assertDictEqual(self.creature.equipment.get(creatures.WEAPONS).inventory, {self.dagger: {'amount': 1}})

    def test_calculate_item_worth(self):
        copper_amount = 10
        bread_amount = 5
        dagger_amount = 5
        self.creature.add_item(self.copper_coin, copper_amount)
        self.creature.add_item(self.bread, bread_amount)
        self.creature.add_item(self.dagger, dagger_amount)

        self.assertEqual(self.creature.calculate_item_worth(self.copper_coin), copper_amount*self.copper_coin.worth)

        self.creature.equip(self.dagger)

        self.assertEqual(self.creature.calculate_item_worth(self.copper_coin), copper_amount*self.copper_coin.worth)
        self.assertEqual(self.creature.calculate_item_worth(self.dagger), dagger_amount*self.dagger.worth)
        self.assertEqual(self.creature.calculate_item_worth(self.bread), bread_amount*self.bread.worth)

    def test_calculate_total_worth(self):
        copper_amount = 10
        bread_amount = 5
        dagger_amount = 5
        self.creature.add_item(self.copper_coin, copper_amount)
        self.creature.add_item(self.bread, bread_amount)
        self.creature.add_item(self.dagger, dagger_amount)
        self.creature.equip(self.dagger)

        result = self.creature.calculate_total_worth()
        answer = (self.copper_coin.worth * copper_amount) + \
                (self.dagger.worth * dagger_amount) + \
                (self.bread.worth * bread_amount)
        self.assertEqual(result, answer)

    def test_type_error(self):
        test_num = 2
        test_string = 'Test'
        test_list = [7]
        test_dict = {"s":2}
        test_tuple = (2, "2")

        test_case = [test_num, test_string, test_list, test_dict, test_tuple, [], {}, ()]
        for case in test_case:
            func = self.creature.add_item
            self.assertRaises(TypeError, func, case)
            self.assertRaises(TypeError, func, (self.dagger, case))
            func = self.creature.remove_item
            self.assertRaises(TypeError, func, case)
            self.assertRaises(TypeError, func, (self.dagger, case))
            func = self.creature.equip
            self.assertRaises(TypeError, func, case)
            func = self.creature.unequip
            self.assertRaises(TypeError, func, case)
            func = self.creature.calculate_item_worth
            self.assertRaises(TypeError, func, case)
            func = self.creature.calculate_total_worth
            self.assertRaises(TypeError, func, case)

    def test_value_error(self):
        test_case = -32

        func = self.creature.add_item
        self.assertRaises(TypeError, func, (self.dagger, test_case))
        func = self.creature.remove_item
        self.assertRaises(TypeError, func, (self.dagger, test_case))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestCreature('test_addItem'))
    return suite


if __name__ == '__main__':
    unittest.main()
    # runner = unittest.TextTestRunner()
    # runner.run(suite())