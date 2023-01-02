class Action:
    I18N = "action.unknown"
    
    def __init__(self, game, player):
        self.game = game
        self.actor = player

class RollDiceAction(Action):
    I18N = "action.roll_dice"

class EndTurnAction(Action):
    I18N = "action.end_turn"

class PayJailAction(Action):
    I18N = "action.pay_jail"

class GetOutJailCardAction(Action):
    I18N = "action.get_out_of_jail_card"

class BuyAction(Action):
    I18N = "action.buy_property"
    
    def __init__(self, game, player, cell):
        super().__init__(game, player)
        self.property = cell

class SellAction(Action):
    I18N = "action.sell_property"

class MortgageAction(Action):
    I18N = "action.mortgage_property"

class LiftMortgageAction(Action):
    I18N = "action.lift_mortgage"

class BuyHouseAction(Action):
    I18N = "action.buy_house"

class SellHouseAction(Action):
    I18N = "action.sell_house"

class BuyHotelAction(Action):
    I18N = "action.buy_hotel"

class SellHotelAction(Action):
    I18N = "action.sell_hotel"