from ..gamelayout import CardGame
from ..cardsets import TYPE
from ..stack import Stack
from ..database import DB


class Klondike(CardGame):

    name = "Klondike"

    def __init__(self):
        """Initialize standard properties of a Klondike game

        Klondike solitaire is your typical single-player solitaire card game
        """
        self.type = TYPE.STANDARD
        self.name = "Klondike"
        self.deckID = -1
        self.wasteID = -1
        self.stacks = []
        self.numrows = 7
        self.numcards = 52
        self.foundations = 4

    def create(self):
        """Create the stacks for the Klondike game"""

        # Create deck and waste stacks
        self.deckID = 0
        self.wasteID = 1
        self.stacks.append(Stack(0, 50, 50, -1, False, 0, [-1]*24, False, deck=True)) # Deck
        self.stacks.append(Stack(1, 100 + 50, 50, -1, False, 0, [], False))  # Waste

        # Create foundation stacks
        stackCount = 2
        for num in range(self.foundations):
            _x = (self.numrows - num + 1) * 80 + 10
            _y = 50
            self.stacks.append(Stack(stackCount, _x, _y, 1, False, 1, [], True, sameSuit=True)) # create foundation stacks
            stackCount += 1

        # Create alternating-suit stacks
        for num in range(self.numrows):
            _x = num * 100 + 50
            _y = 250

            def cards():
                if num == 0:
                    return [1]
                else:
                    return [-1]*(num) + [1]

            self.stacks.append(Stack(stackCount, _x, _y, 13, True, -1, cards(),offset=15))  # create normal stacks
            stackCount += 1

    def deal(self):
        """Perform an in-game deal"""

        deck = self.stacks[self.deckID]
        waste = self.stacks[self.wasteID]
        if len(deck.cards) == 0:
            return # raise NotImplementedError("Recycling deck hasn't been implemented yet.")
        
        for i in range(1, 4):
            card = deck.cards[-i]
            cardImg = deck.cardWidgets[-i]
            deck.cards.pop()
            waste.cards.append(card)
            deck.cardWidgets.pop()
            waste.cardWidgets.append(cardImg)
            cardImg.cardNum = len(waste.cardWidgets) - 1
            cardImg.stackID = waste.ID
        for cardImg in waste.cardWidgets:
            cardImg.place(x=waste.x,
                y=waste.y + cardImg.cardNum * waste.offset)
        card = deck.cardWidgets[-1]
        card.place(x=deck.x,
            y=deck.y + card.cardNum * deck.offset)

DB.add_game("Klondike", Klondike)
