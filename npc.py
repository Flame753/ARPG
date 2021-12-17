import items

class NonPlayableCharacter():
    def __init__(self) -> None:
        raise NotImplementedError("Do not creat raw NPC objects.")

    def __str__(self) -> str:
        return self.name

class Trader(NonPlayableCharacter):
    def __init__(self) -> None:
        self.name = "Trader"
        self.gold = 100
        self.inventory = [items.Bread(),
                            items.Bread(),
                            items.Bread(),
                            items.Bread(),
                            items.HealingPotion(),
                            items.HealingPotion()]
                            