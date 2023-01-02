from action import *
from cells import *
from constants import Constants
from money import Money
from player import Player
from turn_state import TurnState

class Game:
    def __init__(self, manager):
        self.mgr = manager
        self.cells = [
            StartCell(),
            PropertyCell(0, "property.brown.1"),
            CommunityChestCell(),
            PropertyCell(0, "property.brown.2"),
            TaxCell(200),
            RailroadCell("property.railroad.1"),
            PropertyCell(1, "property.light_blue.1"),
            ChanceCell(),
            PropertyCell(1, "property.light_blue.2"),
            PropertyCell(1, "property.light_blue.3"),
            JailCell(),
            PropertyCell(2, "property.pink.1"),
            CompanyCell("property.electric"),
            PropertyCell(2, "property.pink.2"),
            PropertyCell(2, "property.pink.3"),
            RailroadCell("property.railroad.2"),
            PropertyCell(3, "property.orange.1"),
            CommunityChestCell(),
            PropertyCell(3, "property.orange.2"),
            PropertyCell(3, "property.orange.3"),
            ParkingCell(),
            PropertyCell(4, "property.red.1"),
            ChanceCell(),
            PropertyCell(4, "property.red.2"),
            PropertyCell(4, "property.red.3"),
            RailroadCell("property.railroad.3"),
            PropertyCell(5, "property.yellow.1"),
            PropertyCell(5, "property.yellow.2"),
            CompanyCell("property.water"),
            PropertyCell(5, "property.yellow.3"),
            GoToJailCell(),
            PropertyCell(6, "property.green.1"),
            PropertyCell(6, "property.green.2"),
            CommunityChestCell(),
            PropertyCell(6, "property.green.3"),
            RailroadCell("property.railroad.4"),
            ChanceCell(),
            PropertyCell(7, "property.blue.1"),
            TaxCell(100),
            PropertyCell(7, "property.blue.2")
        ]
        
        self.players = []
        for i in range(8):
            player = Player(i)
            player.money[500] = 2
            player.money[100] = 2
            player.money[50] = 2
            player.money[20] = 6
            player.money[10] = 5
            player.money[5] = 5
            player.money[1] = 5
            self.players.append(player)

        self.player = self.players[0]
        
        for cell in self.cells:
            if isinstance(cell, PropertyCell) and cell.owner is not None:
                self.players[cell.owner].properties.append(cell)
        
        self.money_pot = []
        self.turn = 0
        self.turn_state = TurnState.ACTION_CHOICE
        self.start_turn()
    
    def get_cell(self, i):
        cell = self.cells[i]
        n = i%10
        if i < 10:
            x = 10-n
            y = 10
        
        elif i < 20:
            x = 0
            y = 10-n
        
        elif i < 30:
            x = n
            y = 0
        
        else:
            x = 10
            y = n
        
        r = i//10
        
        return (cell, x, y, r)

    def start_turn(self):
        self.turn_state = TurnState.ACTION_CHOICE
        self.player.has_rolled = False
        self.actions = self.get_actions()
    
    def end_turn(self):
        self.turn += 1
        self.turn %= len(self.players)
    
    def get_actions(self):
        if self.turn != self.player.id: return []
        actions = []
        
        player = self.player
        cell = self.get_cell(self.player.pos)
        
        if player.has_rolled:
            actions.append(EndTurnAction(self, player))
        
        if player.in_jail:
            if not player.has_rolled and player.jail_rolls < Constants.MAX_JAIL_ROLLS:
                actions.append(RollDiceAction(self, player))
            
            actions.append(PayJailAction(self, player))
            if player.get_out_of_jail_cards:
                actions.append(GetOutJailCardAction(self, player))
        
        elif not player.has_rolled:
            actions.append(RollDiceAction(self, player))
        
        if isinstance(cell, PropertyCell):
            if cell.owner is None:
                actions.append(BuyAction(self, player, cell))
        
        if player.properties:
            actions.append(SellAction(self, player))
            
            not_mortgaged = list(filter(lambda p: not p.mortgaged, player.properties))
            mortgaged = list(filter(lambda p: p.mortgaged, player.properties))
            house_place = list(filter(lambda p: 0 <= p.get_houses() < 4, player.properties))
            four_houses = list(filter(lambda p: p.get_houses() == 4 and not p.has_hotel(), player.properties))
            hotel = list(filter(lambda p: p.has_hotel(), player.properties))
            
            if not_mortgaged:
                actions.append(MortgageAction(self, player))

            if mortgaged:
                actions.append(LiftMortgageAction(self, player))

            if house_place:
                actions.append(BuyHouseAction(self, player))
            
            if house_place or four_houses:
                actions.append(SellHouseAction(self, player))
            
            if four_houses:
                actions.append(BuyHotelAction(self, player))
            
            if hotel:
                actions.append(SellHotelAction(self, player))
        
        return actions