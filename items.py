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

class Dagger(Weapon):
    def __init__(self) -> None:
        self.name = "Dagger"
        self.description = "A small dagger with some rust. " \
                            "Somewhat more dangerous than a rock."
        self.damage = 10

class RustySword(Weapon):
    def __init__(self) -> None:
        self.name = "Rusty sword"
        self.description = "This sword is showing its age, " \
                            "but still has some fight in it."
        self.damage = 20

class Crossbow(Weapon):
    def __init__(self) -> None:
        self.name = "Crossbow"
        self.description = "Strong and sturdy Crossbow." \
                            "Allows a range attack."
        self.damage = 15

class Axe(Weapon):
    def __init__(self) -> None:
        self.name = "Axe"
        self.description = "This axe is showing its age, " \
                            "but still has some fight in it to do damage."
        self.damage = 25
