# Standard library imports  
import unittest

# Local application imports
from Model.utils import Container, Dice


class TestContainer(unittest.TestCase):
    def test_add_nothing(self):
        c = Container()
        c.add(obj="a")
        self.assertEqual(c.get_inventory(), {"a": {"amount": 0}})

    def test_add_once(self):
        c = Container()
        c.add(obj="a", amount=1)
        self.assertEqual(c.get_inventory(), {"a": {"amount": 1}})

    def test_add_twice(self):
        c = Container()
        c.add(obj="a", amount=1)
        c.add(obj="a", amount=1)
        self.assertEqual(c.get_inventory(), {"a": {"amount": 2}})

    def test_remove_nothing(self):
        c = Container()
        c.add(obj="a", amount=1)
        self.assertTrue(c.remove(obj="a"))
        self.assertEqual(c.get_inventory(), {"a": {"amount": 1}})

    def test_remove_once(self):
        c = Container()
        c.add(obj="a", amount=1)
        c.add(obj="b", amount=1)
        self.assertTrue(c.remove(obj="b", amount=1))
        self.assertEqual(c.get_inventory(), {"a": {"amount": 1}})

    def test_remove_twice(self):
        c = Container()
        c.add(obj="a", amount=2)
        c.add(obj="b", amount=1)
        self.assertTrue(c.remove(obj="b", amount=1))
        self.assertTrue(c.remove(obj="a", amount=2))
        self.assertEqual(c.get_inventory(), {})
    
    def test_remove_something_not_exist(self):
        c = Container()
        c.add(obj="a", amount=2)
        self.assertFalse(c.remove(obj="z", amount=2))
        self.assertEqual(c.get_inventory(), {"a": {"amount": 2}})


class TestDice(unittest.TestCase):
    def test_roll_zero(self):
        with self.assertRaises(ValueError):
            Dice.d2.roll(0)

    def test_roll_Negative_number(self):
        with self.assertRaises(ValueError):
            Dice.d2.roll(-2)
    