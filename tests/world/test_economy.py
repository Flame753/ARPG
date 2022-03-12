# Standard library imports 
from pprint import pprint
import unittest

# Local application imports
from context import world
from world import economy
from entities import currency
from entities import slots


class TestCreatures(unittest.TestCase):
    def test_span(self):
        self.copper = currency.CopperCoin()
        self.silver = currency.SilverCoin()
        self.gold = currency.GoldCoin()
        self.platinum = currency.PlatinumCoin()

    def test_find_vaild_coins(self):
        coin_pouch = slots.Coins()

        print(economy.find_valid_coins(coin_pouch))


if __name__ == '__main__':
    unittest.main()