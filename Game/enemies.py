from creatures import Creature


class Enemy(Creature):
    def __init__(self) -> None:
        raise NotImplementedError("Do not create raw Enemy objects.")
    
    def __str__(self) -> None:
        return self.name

class GiantSpider(Enemy):
    def __init__(self) -> None:
        self.name = "Giant Spider"
        self.hp = 10
        self.damage = 2

class Ogre(Enemy):
    def __init__(self) -> None:
        self.name = "Ogre"
        self.hp = 30
        self.damage = 10

class BatColony(Enemy):
    def __init__(self) -> None:
        self.name = "Colony of bats"
        self.hp = 100
        self.damage = 4

class RockMonster(Enemy):
    def __init__(self) -> None:
        self.name = "Rock Monster"
        self.hp = 80
        self.damage = 15
