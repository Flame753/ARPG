# from Controller.engine import EventEngine
# from View.cli import CLI
# from Model.player import Player, create_player
# from Model.story_pieces import RoadEvents

# BridHunt = RoadEvents.BridHunt_White
# BrokenCart = RoadEvents.BrokenCart
# player = create_player("Test_name")
# ui = CLI()

# # EventEngine.interact_with_player(ui, player, BridHunt.value)
# # EventEngine.interact_with_player(ui, player, BrokenCart.value)
# # print(player.hp, player.get_inventory())




# from Model.creature import Creature, Enemy
# from Model.story_pieces import Situation, RoadEvents, BridHunt, breakingtest

# # s = Situation(text="h")
# # print(s, s.id)
# # s = Situation(text="h")
# # print(s, s.id)
# # s = Situation(text="h")
# # print(s, s.id)
# # print(s, s.id)


# print(RoadEvents.bad.value.situation.id)
# print(RoadEvents.bad.value.situation.id)
# # print(RoadEvents.BridHunt.value.situation.id)
# print(RoadEvents.BrokenCart.value.situation.id)
# #creating new instances
# # print(BridHunt().situation.id)
# print(breakingtest().situation.id)
# print(breakingtest().situation.id)
# print(breakingtest().situation.id)
# # from itertools import count
# # counter = count(0, 1)
# # print(counter.__next__())
# # print(counter.__next__())
# # print(counter.__next__())
# # print(counter.__next__())
# # print(counter.__next__())
# # print(counter.__next__())
# # print(counter.__next__())

# # print(RoadEvents.BridHunt.value.situation.id)

# from Model.utils import Color
# template = "You see a flock of {color} bird flying over head. " \
#             "It seem like a great change to get a easy meal. "

# print(Color.Black.name)
# print(template.format(color=Color.Red.name.lower()))


# from Model.outcome_effects import TakenDamage, OUTCOME_EFFECTS, OutcomeEffects
# TakenDamage2 = OUTCOME_EFFECTS.get(OutcomeEffects.TakenDamage)
# print(TakenDamage(amount=1).modify_player(player))

# print(TakenDamage2(2).modify_player(player))


# Standard library imports  
# from dataclasses import dataclass, field
# from typing import Optional
# from abc import ABC, abstractmethod
# import enum

# # Local application imports
# from Model.player import Player
# from Model.utils import Dice



# class Effect(ABC):  
#     @abstractmethod
#     def modify_player(self, player: Player) -> None:
#         ...


# @dataclass
# class TakenDamage(Effect):
#     amount: int
#     def modify_player(self, player: Player) -> None:
#         player.hp.restore(-self.amount)
#         print("--------> Test print: (in outcome_effect module) ", player.hp.current )


# @dataclass
# class RestoreHealth(TakenDamage):
#     def modify_player(self, player: Player) -> None:
#         player.hp.restore(self.amount)


# @dataclass
# class ReceiveReward(Effect):
#     item: str
#     amount: int
#     def modify_player(self, player: Player) -> None:
#         player.add(self.item, self.amount)


# @dataclass
# class LostItem(ReceiveReward):
#     def modify_player(self, player: Player) -> None:
#         player.remove(self.item, self.amount)


# class OutcomeEffects(enum.Enum):
#     TakenDamage = "Taken Damage"
#     RestoreHealth = "Restore Health"
#     ReceiveReward = "Receive Reward"
#     LostItem = "Lost Item"


# OUTCOME_EFFECTS: dict[OutcomeEffects, type[Effect]] = {
#     OutcomeEffects.TakenDamage: TakenDamage,
#     OutcomeEffects.RestoreHealth: RestoreHealth,
#     OutcomeEffects.ReceiveReward: ReceiveReward,
#     OutcomeEffects.LostItem: LostItem}


# class of(enum.Enum):
#     TakenDamage = TakenDamage
#     RestoreHealth = RestoreHealth
#     ReceiveReward = ReceiveReward
#     LostItem = LostItem


# print(of.TakenDamage.value(2))


# from Model.creature import Enemy, Creature
# from Model.stats import CapacityStat

# print(Enemy.BatColony())

# print(Enemy.GiantSpider)

# a = Enemy.BatColony()
# b = Enemy.BatColony()
# c = Enemy.BatColony()
# b.inventory.add("str", 2)
# print(a)
# print("b", b.inventory.get_all())
# print("c", c.inventory.get_all())
# print("all", Enemy.BatColony().inventory.get_all())

# d = Creature("Giant Spider", hp=CapacityStat(10, .2), mana=CapacityStat(0, 0), stamina=CapacityStat(30, .5))
# e = Creature("Giant Spider", hp=CapacityStat(10, .2), mana=CapacityStat(0, 0), stamina=CapacityStat(30, .5))

# d.inventory.add("Cap")
# e.inventory.add("same")

# print("d", d.inventory.get_all())
# print("e", e.inventory.get_all())

from pprint import pprint
from Model.experience import Algorithms
# pprint(Enemy.__dict__)

# from Model.player import create_player
# p = create_player("s")
# p.inventory.add("s", 2)
# print(p.inventory.get_all())

from Model.stats import CoreStat, Stats, PrimaryStat

# st = Stats()
# pprint(st.core)
# con = st.core.get(CoreStat.Con).get("level")
# str = st.core.get(CoreStat.Str).get("level")

# con.add_xp(13000)
# print(con.xp)
# print(con.get_level())
# vigor = st.primary.get(PrimaryStat.Vigor)
# pprint(vigor.current_value)
# vigor.update()
# pprint(vigor.current_value)

# str.add_xp(3000)
# pprint(vigor.current_value)
# vigor.update()
# pprint(vigor.current_value)

# import math
# stat = Stats()

# stat.points = 220
# print("points: ", stat.points)
# print("core stats: ")
# pprint(stat.core)
# print("core stats: ________________________")
# stat.apply_points(CoreStat.Con, 220)
# stat.apply_xp(CoreStat.Con, 500)
# stat.apply_xp(CoreStat.Con, 500)
# stat.apply_xp(CoreStat.Con, 500)
# stat.apply_xp(CoreStat.Con, 500)
# stat.apply_xp(CoreStat.Con, 500)
# pprint(stat.core)
# print(stat.get_level(CoreStat.Con))

# print(stat.primary.get(PrimaryStat.Vigor).current_value)
# stat.update()
# print(stat.primary.get(PrimaryStat.Vigor).current_value)
# print(stat.primary.get(PrimaryStat.Vigor).loss(5))
# print(stat.primary.get(PrimaryStat.Vigor).current_value)
# print(stat.primary.get(PrimaryStat.Vigor).loss(15))
# print(stat.primary.get(PrimaryStat.Vigor).current_value)

# f = lambda x: 55 * (x ** 3) 
# fn =lambda x: (x/55)**(1/3)
# for x in range(0, 441):
#     print(x, ": ", f(x), fn(x))


from Model.creature import Creature

c = Creature(name="s")
# c2 = Creature(name="c")
c.level.add_xp(234)
print("current xp", c.level.xp)
print("current level", c.level.get_level())
# print(c2.level.xp)
print("amount to next level", c.level.amount_to_next_level())

# from Model.experience import Algorithm

# print(Algorithm.Stats(235))

for x in range(0, 441):
    print(x, ": ", "level:", Algorithms.Creature.value.reverse(x), "xp:", Algorithms.Creature.value.formula(x))