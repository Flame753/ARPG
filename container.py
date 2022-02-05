from abc import ABC
from dataclasses import dataclass, field


@dataclass
class Container(ABC):
    container: dict = field(default_factory=dict, init=False)

    def update(self, dict_of_items: dict):
        self.container.update(dict_of_items)
    
    def addItem(self, item, amount=0):
        if item in self.container:
            self.container[item]['amount'] += amount
        else:
            self.container[item] = {'amount': amount}
    
    def removeItem(self, item, amount = 0):
        if item in self.container:
            if self.container[item]['amount'] >= amount:
                self.container[item]['amount'] -= amount
                if self.container[item]['amount'] == 0:
                    del(self.container[item])
                return True
        return False

    def calculateItemWeight(self, item):
        if item in self.container:
            return item.weight * self.container[item]['amount']
        return 0

    def calculateItemWorth(self, item):
        if item in self.container:
            return item.worth * self.container[item]['amount']
        return 0

    def calculateTotalWeight(self):
        weight = 0
        for item, data in self.container.items():
            weight += item.weight * data['amount']
        return weight

    def calculateTotalWorth(self):
        worth = 0
        for item, data in self.container.items():
            worth += item.worth * data['amount']
        return worth


def main():
    import items
    i = Container()
    i2 = Container()
    print(i == i2)
    print(i is i2)

    # print(i.container)
    a = items.Bread()
    b = items.Bread()
    c = items.Bread()
    i.addItem(a, 2)

    print(i == i2)
    print(i is i2)
    # print(i.container)

    # print(a, b, c)
    # print(a, b, c)







if __name__ == "__main__":
    main()
