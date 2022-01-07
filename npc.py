import items
from creatures import Creature
from abc import ABC


class NonPlayableCharacter(Creature):
    def __init__(self, name, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name
        if type(self) == Creature:
            raise Exception('Do not instantiate NonPlayableCharacter directly')

    def __str__(self) -> str:
        return self.name

class Trader(NonPlayableCharacter):
    def __init__(self, **kwargs):
        super().__init__(name="Trader", **kwargs)
        
        self.gold = 100

        self.addItem(items.CoinPouch(), 2)
        self.addItem(items.GoldCoin(), 100)
        self.addItem(items.Backpack())
        self.addItem(items.Bread(), 4)
        self.addItem(items.HealingPotion(), 2)

if __name__ == "__main__":
    t = Trader()
    print(t.name)
    # print(t.getAllItems())                           