from world.tiles import TraderTile
from entities import npc
from player import Player
from pprint import pprint
from entities import slots
from entities import creatures
# player = Player()
# t = TraderTile(1, 1)
# t.trade(npc.Trader(), player)

# print(creatures.Creature())

from entities.currency import CopperCoin, SilverCoin, GoldCoin, PlatinumCoin, GreaterPlatinumCoin

from entities.slots import Coins

# c = Coins()
# print(c.haveCoin(CopperCoin()))
# c.add_item(CopperCoin())
# print(c.haveCoin(CopperCoin()))
# c.add_item(SilverCoin(), 203)
# print(c.haveCoin(SilverCoin(), 204))
# print(c.haveCoin(SilverCoin(), 200))

# print(CopperCoin == SilverCoin)
# pprint(CopperCoin.__dict__)
# print('_'*30)
# pprint(CopperCoin() == CopperCoin())


# print(slots.Miscellaneous == slots.Miscellaneous)
# pprint(slots.Miscellaneous.__dict__)
# print('_'*30)
# pprint(slots.Miscellaneous() == slots.Miscellaneous())
# print({slots.Miscellaneous:2})

# # print({CopperCoin(): 2})

# d = Dagger()
# print(d, d.coin_type)



# class d():
#     def __init__(self) -> None:
#         # self.test = ("amount", "coin_type")
#         self.test = {"value": "amount", "coin_type": "type"}


# # a = d().test
# # print(a["value"])
# b, c = d().test
# print(b)
# print(c)

from world.economy import exchange, exchange2, price_to_coin_converstion, ALL_CURRENCY, STANDARD_CURRENCY

c = CopperCoin()
s = SilverCoin()
g = GoldCoin()
p = PlatinumCoin()
# print(exchange(20, g, c))
# print(exchange2(20, g, c))

pouch = slots.Coins()
pouch.add_item(c, 6)
pouch.add_item(g, 2)
pouch.add_item(s, 8)
# pouch.add_item(GreaterPlatinumCoin(), 8)

pouch.order(reverse=True)
print(pouch.container)
# pprint(price_to_coin_converstion(2860, pouch))




# def min_subarray_sum(array):
#     if len(array) == 0:
#         return 0
#     min_sum = float("inf")
#     for i in range(len(array)):
#         for j in range(i + 1, len(array) + 1):
#             subarray = array[i: j]
#             print(subarray)
#             min_sum = min(min_sum, sum(subarray))

#     return min_sum

# min_subarray_sum([-7, 3, 4, -2, -3, 1, -3])