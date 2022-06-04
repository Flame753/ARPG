import unittest
from Model.economy import Currency


class TestCurrency(unittest.TestCase):
    # Currency Conversion Method
    def test_currency_conversion_zero(self):
        answer = {Currency.Platinum: 0, Currency.Gold: 0, Currency.Silver: 0, Currency.Copper: 0}
        self.assertEqual(Currency.currency_conversion(), answer)
    
    def test_currency_conversion_2325(self):
        answer = {Currency.Platinum: 1, Currency.Gold: 1, Currency.Silver: 1, Currency.Copper: 1}
        self.assertEqual(Currency.currency_conversion(1111), answer)
    
    def test_currency_conversion_type_error(self):
        with self.assertRaises(TypeError):
            Currency.currency_conversion("1111")

    def test_currency_conversion_value_error(self):
        with self.assertRaises(ValueError):
            Currency.currency_conversion(-1)

    # Integer Conversion Method
    def test_integer_conversion(self):
        coins = {Currency.Platinum: 1, Currency.Gold: 1, Currency.Silver: 1, Currency.Copper: 1}
        self.assertEqual(Currency.integer_conversion(coins=coins), 1111)

    def test_integer_conversion_type_error(self):
        with self.assertRaises(TypeError):
            Currency.integer_conversion(coins="coins")

    # Exchange Method
    def test_exchange_copper_to_silver(self):
        answer = {Currency.Silver: 1, Currency.Copper: 0}
        self.assertEqual(Currency.exchange(10, Currency.Copper, Currency.Silver), answer)

    def test_exchange_gold_to_silver(self):
        answer = {Currency.Silver: 10, Currency.Gold: 0}
        self.assertEqual(Currency.exchange(1, Currency.Gold, Currency.Silver), answer)
    
    def test_exchange_copper_to_gold(self):
        answer = {Currency.Copper: 1, Currency.Gold: 1}
        self.assertEqual(Currency.exchange(101, Currency.Copper, Currency.Gold), answer)

    def test_exchange_type_error(self):
        with self.assertRaises(TypeError):
            Currency.exchange(101, Currency.Copper, "Gold")
    
    def test_exchange_value_error(self):
        with self.assertRaises(ValueError):
            Currency.exchange(-1, Currency.Copper, Currency.Gold)