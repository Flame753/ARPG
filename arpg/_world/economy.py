# Local application imports
from entities.items import CopperCoin, GreaterCopperCoin
from entities.items import SilverCoin, GreaterSilverCoin
from entities.items import GoldCoin, GreaterGoldCoin
from entities.items import PlatinumCoin, GreaterPlatinumCoin



def exchange(amount, coin_one, coin_two):
    # Exchange the amount of coin one into the equal value of coin two if possible
    total_value_of_coin_one = coin_one.worth * amount
    amount_of_coin_two = total_value_of_coin_one // coin_two.worth
    total_value_of_coin_two = amount_of_coin_two * coin_two.worth
    total_value_of_coin_one -= total_value_of_coin_two
    amount_of_coin_one = total_value_of_coin_one // coin_one.worth
    return [(amount_of_coin_one, coin_one),(amount_of_coin_two, coin_two)]
