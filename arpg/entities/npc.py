from entities import items
from entities import currency
from entities.creatures import Creature



class NonPlayableCharacter(Creature):
    def __init__(self, name, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name
        if type(self) == Creature:
            raise NotImplementedError('Do not instantiate NonPlayableCharacter directly')

    def __str__(self) -> str:
        return self.name

class Trader(NonPlayableCharacter):
    def __init__(self, **kwargs):
        super().__init__(name="Trader", **kwargs)

        # self.addItem(items.CoinPouch(sellable=False), 2)
        self.addItem(currency.GoldCoin(), 100)
        # self.addItem(items.Backpack(sellable=False))
        self.addItem(items.Bread(), 4)
        self.addItem(items.HealingPotion(), 2)
