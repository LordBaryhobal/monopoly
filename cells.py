import random

from colors import Colors

class Cell:
    def __init__(self):
        self.rect = [0, 0, 0, 0]
    
    def as_owner(self, player):
        pass
    
    def as_visitor(self, player):
        pass

    def as_client(self, player):
        pass

class PropertyCell(Cell):
    COLORS = [
        Colors.BROWN,
        Colors.LBLUE,
        Colors.PINK,
        Colors.ORANGE,
        Colors.RED,
        Colors.YELLOW,
        Colors.GREEN,
        Colors.BLUE
    ]
    
    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.owner = None
        self.owner = random.randint(-1, 7)
        if self.owner == -1: self.owner = None
        
        self.mortgaged = False
        self.houses = 0
        self.hotel = False
    
    def get_color(self):
        return PropertyCell.COLORS[self.color]
    
    def get_houses(self):
        return self.houses
    
    def has_hotel(self):
        return self.hotel

class SpecialPropertyCell(PropertyCell):
    def __init__(self, name):
        super().__init__(-1, name)
        self.houses = -1
    
    def get_color(self):
        return (0,0,0)

class RailroadCell(SpecialPropertyCell):
    pass

class CompanyCell(SpecialPropertyCell):
    pass

class TaxCell(Cell):
    def __init__(self, amount):
        self.amount = amount

class StartCell(Cell):
    pass

class CommunityChestCell(Cell):
    pass

class ChanceCell(Cell):
    pass

class JailCell(Cell):
    pass

class ParkingCell(Cell):
    pass

class GoToJailCell(Cell):
    pass