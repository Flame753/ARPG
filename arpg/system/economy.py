# Local application imports
from entities.currency import Coin
from entities.currency import CopperCoin, GreaterCopperCoin
from entities.currency import SilverCoin, GreaterSilverCoin
from entities.currency import GoldCoin, GreaterGoldCoin
from entities.currency import PlatinumCoin, GreaterPlatinumCoin
from entities import slots



ALL_CURRENCY = [CopperCoin(), GreaterCopperCoin(), 
                SilverCoin(), GreaterSilverCoin(),
                GoldCoin(), GreaterGoldCoin(),
                PlatinumCoin(), GreaterPlatinumCoin()]

STANDARD_CURRENCY = [CopperCoin(), 
                    SilverCoin(),
                    GoldCoin(),
                    PlatinumCoin()]



class UnaffordableError(Exception):
    """Exception raised for if an item is too expensive."""
    
    def __init__(self, message="Item is too expensive to buy!"):
        self.message = message
        super().__init__(self.message)



def exchange(amount, coin_one, coin_two):
    # Exchange the amount of coin one into the equal value of coin two if possible
    total_value_of_coin_one = coin_one.worth * amount
    amount_of_coin_two = total_value_of_coin_one // coin_two.worth
    total_value_of_coin_two = amount_of_coin_two * coin_two.worth
    total_value_of_coin_one -= total_value_of_coin_two
    amount_of_coin_one = total_value_of_coin_one // coin_one.worth
    return [(amount_of_coin_one, coin_one),(amount_of_coin_two, coin_two)]

def exchange2(amount, coin_one, coin_two):
    return (amount * coin_one.worth) // coin_two.worth


def find_valid_coins(coin_slot: slots.Coins) -> list[Coin]:
    valid_coins = list()
    coin_in_slot = coin_slot.find_largest_coin()
    
    if not coin_in_slot: 
        valid_coins.append(CopperCoin())
        return valid_coins

    for coin in reversed(STANDARD_CURRENCY):
        if coin.worth <= coin_in_slot.worth:
            valid_coins.append(coin)
    return valid_coins

def remove_all_zeros(coins: dict[Coin]) -> dict[Coin]:
    # Removes any amount of a coin completely if the amount is zero
    # Modifies original dict of coins and return a new dict of coins 
    copy_of_coins = coins.copy()
    coins.clear()
    for coin, amount in copy_of_coins.items():
        if amount != 0: coins.update({coin: amount})
    return coin

def price_to_coin_converstion(price: int, coin_slot: slots.Coins) -> dict[Coin]:
    # Returns a dict of coins with there respected amount to equal the total price
    valid_converstion = dict()
    vaild_coins = find_valid_coins(coin_slot)
    for coin in vaild_coins:
        amount = price // coin.worth
        price = price - (amount * coin.worth) # Remaining Amount 
        valid_converstion[coin] = amount
    return valid_converstion

def item_expensive(item_price: int, current_amount: int) -> bool:
    return item_price > current_amount

def transaction(seller, buyer, item):
    buyer_wealth = buyer.coin_pouch.calculate_total_worth()
    
    if item_expensive(item.worth, buyer_wealth):
        raise UnaffordableError

    price_as_coins = price_to_coin_converstion(item.worth, buyer.coin_pouch)
    remove_all_zeros(price_as_coins)

    # for coin, amount in price_as_coins.items():
    #     buyer_amount = coin.get()

    for coin, amount in price_as_coins.items():
        seller.coin_pouch.add_item(coin, amount)
        buyer.coin_pouch.remove_item(coin, amount)
        # Buyer issue. if buyer has not exact coin amount
        # Like item worth 86 and buyer had only 9 silver.
        # Or buyer had one gold and items is still worth 86 (80 silver and 6 copper)

