import random

from colors import Colors

class Player:
    COLORS = [
        Colors.PLAYER_0,
        Colors.PLAYER_1,
        Colors.PLAYER_2,
        Colors.PLAYER_3,
        Colors.PLAYER_4,
        Colors.PLAYER_5,
        Colors.PLAYER_6,
        Colors.PLAYER_7
    ]
    
    def __init__(self, id_):
        self.id = id_
        self.pos = 0
        #self.pos = random.randint(0, 39)
        self.money = {}
        self.properties = []
        self.doubles = 0
        self.in_jail = False
        self.jail_rolls = 0
        self.get_out_of_jail_cards = 0
        self.has_rolled = False
    
    def get_color(self):
        return self.COLORS[self.id]
    
    def get_money(self):
        return sum(map(lambda v: v[0]*v[1], self.money.items()))
    