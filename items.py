class Weapon:
    def __init__(self) -> None:
        raise NotImplementedError("Do not create raw Weapon objects.")

    def __str__(self) -> str:
        return self.name

class Rock(Weapon):
    def __init__(self) -> None:
        self.name = 'Rock'
        self.description = "A fist-sized rock, suitable for bludgeoning."
        self.damage = 5
        self.value = 1

class Dagger(Weapon):
    def __init__(self) -> None:
        self.name = "Dagger"
        self.description = "A small dagger with some rust. " \
                            "Somewhat more dangerous than a rock."
        self.damage = 10
        self.value = 20


class RustySword(Weapon):
    def __init__(self) -> None:
        self.name = "Rusty sword"
        self.description = "This sword is showing its age, " \
                            "but still has some fight in it."
        self.damage = 20
        self.value = 100

class Crossbow(Weapon):
    def __init__(self) -> None:
        self.name = "Crossbow"
        self.description = "Strong and sturdy Crossbow." \
                            "Allows a range attack."
        self.damage = 15
        self.value = 75

class Axe(Weapon):
    def __init__(self) -> None:
        self.name = "Axe"
        self.description = "This axe is showing its age, " \
                            "but still has some fight in it to do damage."
        self.damage = 25
        self.value = 60


class Consumable:
    def __init__(self) -> None:
        raise NotImplementedError("Do not create raw Consumable objects.")
    
    def __str__(self) -> str:
        return "{} (+{} HP)".format(self.name, self.healing_value)

class CrustyBread(Consumable):
    def __init__(self) -> None:
        self.name = "Crusty Bread"
        self.healing_value = 10
        self.value = 12

class HealingPotion(Consumable):
    def __init__(self) -> None:
        self.name = "Healing Potion"
        self.healing_value = 50
        self.value = 60
