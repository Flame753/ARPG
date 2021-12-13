class Creature:
    def __init__(self) -> None:
        raise NotImplementedError("Do not create raw Creatrue objects.")

    def is_alive(self):
        return self.hp > 0