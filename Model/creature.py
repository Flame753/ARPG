from dataclasses import dataclass
import enum



class Creature():
    def __init__(self, name: str, max_hp: int, damage: int) -> None:
        self.name = name
        self.hp = max_hp
        self.max_hp = max_hp
        self.damage = damage

    def is_alive(self) -> bool:
        return self.hp > 0


class Enemy(enum.Enum):
    GiantSpider = Creature("Giant Spider", max_hp=10, damage=2)
    Ogre = Creature("Ogre", max_hp=30, damage=10)
    BatColony = Creature("Bat of Colony", max_hp=100, damage=4)
    RockMonster = Creature("Rock Monster", max_hp=80, damage=15)


print(list(Enemy))

