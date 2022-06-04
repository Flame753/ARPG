# Standard library imports  
from dataclasses import dataclass, field
from typing import Optional
from abc import ABC
import enum


# Local application imports


# Type Aliases
Coin = enum.IntEnum


# class UnaffordableError(Exception):
#     """Exception raised for if an item is too expensive."""
    
#     def __init__(self, message="Item is too expensive to buy!"):
#         self.message = message
#         super().__init__(self.message)


class Currency(enum.IntEnum):
    Copper = 1
    Silver = 10
    Gold = 100
    Platinum = 1000

    @classmethod
    def currency_conversion(cls, number: int=0) -> dict[Coin, int]:
        if not isinstance(number, int):
            raise TypeError(f"Incorrect Type: {type(number)}. Perimeter should be a Integer!")
        if number < 0:
            raise ValueError(f"Negative Numbers are invalid: ({number})")

        coins = {}

        for coin in reversed(cls):
            amount = number // coin.value
            remainder = number % coin.value
            coins.update({coin: amount})
            number = remainder

        return coins

    @classmethod
    def integer_conversion(cls, coins:dict[Coin, int]) -> int:
        if not isinstance(coins, dict):
            raise TypeError(f"Incorrect Type: {type(coins)}. Perimeter should be a Dictionary," +
                            "containing coins as keys and the amount of coins as an integer!")

        amount = 0 
        for coin in cls:
            amount += (coin.value * coins.get(coin))

        return amount

    @staticmethod
    def exchange(amount: int, coin1: Coin, coin2: Coin) -> dict[Coin, int]:
        if not isinstance(amount, int) or not isinstance(coin1, Currency) or not isinstance(coin2, Currency):
            raise TypeError("One of the Arguments is the wrong type! amount: " +  
                            f"{type(amount)}, coin1: {type(coin1)}, coin2: {type(coin2)}")
        if amount < 0:
            raise ValueError(f"Negative Numbers are invalid: ({amount})")

        amount_of_coin2 = (amount * coin1.value) // coin2.value
        amount_of_coin1 = ((amount * coin1.value) - (amount_of_coin2 * coin2.value)) // coin1.value
        return {coin1: amount_of_coin1, coin2: amount_of_coin2}

    @classmethod
    def exhange_down(cls, number: int, convert_to: Coin):
        """Converts a number into a dictionary. Contains different currency types with a corressponding amount.
        Any large currency value that is over the <cover_to> perimeter will be converted into that currency type. """
        coins = cls.currency_conversion(number)

        for coin, amount in coins.items():
            if coin == convert_to:
                break
            new = cls.exchange(amount, coin, convert_to)

        coins.update(new)
        return coins


# def find_valid_coins(coin_slot: slots.Coins) -> list[Coin]:
#     valid_coins = list()
#     coin_in_slot = coin_slot.find_largest_coin()
    
#     if not coin_in_slot: 
#         valid_coins.append(CopperCoin())
#         return valid_coins

#     for coin in reversed(STANDARD_CURRENCY):
#         if coin.worth <= coin_in_slot.worth:
#             valid_coins.append(coin)
#     return valid_coins

# def remove_all_zeros(coins: dict[Coin]) -> dict[Coin]:
#     # Removes any amount of a coin completely if the amount is zero
#     # Modifies original dict of coins and return a new dict of coins 
#     copy_of_coins = coins.copy()
#     coins.clear()
#     for coin, amount in copy_of_coins.items():
#         if amount != 0: coins.update({coin: amount})
#     return coin

# def price_to_coin_converstion(price: int, coin_slot: slots.Coins) -> dict[Coin]:
#     # Returns a dict of coins with there respected amount to equal the total price
#     valid_converstion = dict()
#     vaild_coins = find_valid_coins(coin_slot)
#     for coin in vaild_coins:
#         amount = price // coin.worth
#         price = price - (amount * coin.worth) # Remaining Amount 
#         valid_converstion[coin] = amount
#     return valid_converstion

# def item_expensive(item_price: int, current_amount: int) -> bool:
#     return item_price > current_amount

# def transaction(seller, buyer, item):
#     buyer_wealth = buyer.coin_pouch.calculate_total_worth()
    
#     if item_expensive(item.worth, buyer_wealth):
#         raise UnaffordableError

#     price_as_coins = price_to_coin_converstion(item.worth, buyer.coin_pouch)
#     remove_all_zeros(price_as_coins)

#     # for coin, amount in price_as_coins.items():
#     #     buyer_amount = coin.get()

#     for coin, amount in price_as_coins.items():
#         seller.coin_pouch.add_item(coin, amount)
#         buyer.coin_pouch.remove_item(coin, amount)
#         # Buyer issue. if buyer has not exact coin amount
#         # Like item worth 86 and buyer had only 9 silver.
#         # Or buyer had one gold and items is still worth 86 (80 silver and 6 copper)
