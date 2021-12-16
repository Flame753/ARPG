from abc import ABC

class BaseItem(ABC):
    def __init__(self, name = None, worth = 0, weight = 0, description = None, **kwargs):
        if type(self) == BaseItem:
            raise Exception('Do not instantiate BaseItem directly')
        self.name = name
        self.worth = worth
        self.weight = weight
        self.description = description

    def __repr__(self):
        return f'{self.__class__.__name__}()'

class CustomWeapon(BaseItem):
    def __init__(self, damage = 0, **kwargs):
        super().__init__(**kwargs)
        self.damage = damage

    def __str__(self):
        return f'{str(self.name)} damage: {str(self.damage)}'

class Rock(CustomWeapon):
    def __init__(self, **kwargs):
        super().__init__(name = 'Rock',
                        damage = 5,
                        worth = 1,
                        weight = 1,
                        description = "A fist-sized rock, suitable for bludgeoning.",
                        **kwargs)

class Dagger(CustomWeapon):
    def __init__(self, **kwargs):
        super().__init__(name = 'Dagger',
                        damage = 10,
                        worth = 20,
                        weight = 1,
                        description = "A small dagger with some rust. " \
                            "Somewhat more dangerous than a rock.",
                        **kwargs)

class RustySword(CustomWeapon):
    def __init__(self, **kwargs):
        super().__init__(name = "Rusty sword",
                        damage = 20,
                        worth = 100,
                        weight = 1,
                        description = "This sword is showing its age, " \
                            "but still has some fight in it.",
                        **kwargs)

class Crossbow(CustomWeapon):
    def __init__(self, **kwargs):
        super().__init__(name = "Crossbow",
                        damage = 15,
                        worth = 75,
                        weight = 2,
                        description = "Strong and sturdy Crossbow." \
                            "Allows a range attack.",
                        **kwargs)

class Axe(CustomWeapon):
    def __init__(self, **kwargs):
        super().__init__(name = "Axe",
                        damage = 25,
                        worth = 60,
                        weight = 2,
                        description = "This axe is showing its age, " \
                            "but still has some fight in it to do damage.",
                        **kwargs)

class CustomConsumable(BaseItem):
    def __init__(self, healing_value = 0, **kwargs):
        super().__init__(**kwargs)
        self.healing_value = healing_value
    
    def __str__(self) -> str:
        return "{} (+{} HP)".format(self.name, self.healing_value)

class CrustyBread(CustomConsumable):
    def __init__(self, **kwargs):
        super().__init__(name = "Crusty Bread",
                        healing_value = 10,
                        worth = 12,
                        weight = 1,
                        description = "Crusty Bread that is not fresh.",
                        **kwargs)

class HealingPotion(CustomConsumable):
    def __init__(self, **kwargs):
        super().__init__(name = "Healing Potion",
                        healing_value = 50,
                        worth = 60,
                        weight = 1,
                        description = "Red shiny liquid in a glass bottle.",
                        **kwargs)


if __name__ == "__main__":
    # BaseItem()
    
    w = Rock()
    d = Dagger()
    print(w, d)
    print([w, d])
    print(w.worth)
