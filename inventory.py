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
    
    def isEmpty(self):
        return True if not self.__dict__ else False

    def isBagEmpty(self):
        return True if not self.bag.__dict__ else False

    def changeEquipment(self, **kwargs):
        # Changes current equipment out with new one
        for key, value in kwargs.items():
            if not hasattr(self, key):
                return False
            if value:
                # Returns Equipment back into bag
                self.bag.addItem(self.__dict__[key], 1)
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
    i = Inventory(bag = items.Backpack(), main_hand=items.Dagger())
    i.changeEquipment(main_hand=items.Rock())
    print(i.__dict__)
    print(i.bag.inventory)
    print(i.calulateWeight())
    print(i.calulateWorth())