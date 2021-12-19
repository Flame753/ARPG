class Inventory:
    def __init__(self, head=None, neck=None, chest=None, 
                waist=None, legs=None, feet=None, hands=None, 
                main_hand=None, off_hand=None, bag=None):
            
        self.head = head
        self.neck = neck
        self.chest = chest
        self.waist = waist
        self.legs = legs
        self.feet = feet
        self.hands = hands
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.bag = bag
    
    def isempty(self):
        return True if not self.__dict__ else False

    def changeWornItem(self, **kwargs):
        for key in kwargs.keys():
            if not hasattr(self, key):
                return False

        self.__dict__.update(kwargs)
        return True

    def addItemsToBag(self, items):
        for item, amount in items.items():
            self.bag.addItem(item, amount)

    def calulateWeight(self):
        weight = 0
        for value in self.__dict__.values():
            if value:
                weight += value.weight
        
        if self.bag:
            weight += self.bag.calculateTotalWeight()

        return weight

    def calulateWorth(self):
        worth = 0
        for value in self.__dict__.values():
            if value:
                worth += value.worth
        
        if self.bag:
            worth += self.bag.calculateTotalWorth()

        return worth

if __name__ == '__main__':
    import items
    i = Inventory(bag = items.Backpack())

    print(i.__dict__)
    print(i.calulateWeight())
    print(i.calulateWorth())