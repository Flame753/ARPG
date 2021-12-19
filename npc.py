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
        self.bag = items.Backpack()

        starting_equipment = {items.Bread(): 4,
                            items.HealingPotion(): 2}
        self.bag.addItems(starting_equipment)

                            