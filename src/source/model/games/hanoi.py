"""Defines the rules and properties of the hanoi game

    State Variables: none

    Environment Variables: none

    Assumptions: none

"""

from ..gamelayout import CardGame
from ..cardsets import TYPE
from ..card import StandardCard
from ..stack import Stack
from ..database import DB


class Hanoi(CardGame):

    name = "Hanoi4"

    def __init__(self, num_cards=4):
        """Initialize standard properties of a 4-card Hanoi game

        Hanoi games are card-based representations of the well-known
        Tower of Hanoi logic puzzle
        """
        self.type = TYPE.STANDARD
        self.name = "Hanoi" + str(num_cards)
        self.deckID = -1
        self.wasteID = -1
        self.stacks = []
        self.numrows = 3
        self.numcards = num_cards
        self.foundations = 0

     # Stack(id, x, y, base, alternate, direction, pos, accept = True)
    def create(self):
        """Create the stacks (left, middle, right) for the Hanoi game"""
        self.stacks.append(Stack(0, 150, 250, -1, False, -1, [1]*self.numcards, True, offset=15))
        self.stacks.append(Stack(0, 350, 250, -1, False, -1, [], True, offset=15))
        self.stacks.append(Stack(0, 550, 250, -1, False, -1, [], True, offset=15))
        self._init_bindings()

    def _init_bindings(self):
        """Initialize mouse bindings"""
        from ..mouse_handler import Bindings
        self._bindings = Bindings(self)
        self._bindings.add("<B1-Motion>", lambda event: Bindings.default_drag(self._bindings, event))
        self._bindings.add("<ButtonRelease-1>", lambda event: Bindings.default_move(self._bindings, event))

    def startDeal(self, cardset):
        """Perform initial deal of cards

        Create and assign :class: `StandardCard` instances to the stacks
        that they belong in (4 cards in the leftmost (0-index) stack)
        """
        for rank in range(0,self.numcards):
            self.stacks[0].cards[rank] = (StandardCard(cardset, self.numcards-rank-1, "h"))
            self.stacks[0].cards[rank].show()

    def valid_drop(self, stackID, destID, cardNum):
        """Indicate whether the selected cards can be moved to the destination stack"""
        if len(self.stacks[destID].cards) == 0:
            return True
        card = self.stacks[stackID].cards[cardNum]
        if self.stacks[destID].cards[-1].rank < card.rank:
            return False
        return True

    def solve(self):
        from ..stack import move_cards
        _start = ("start", self.stacks[0].cards)
        _spare = ("spare", self.stacks[1].cards)
        _dest = ("dest", self.stacks[2].cards)

        def move(self, start, end, card):
            if start == "start":
                startID = 0
            elif start == "spare":
                startID = 1
            else:
                startID = 2
            if end == "start":
                endID = 0
            elif end == "spare":
                endID = 1
            else:
                endID = 2
            move_cards(self, startID, endID, card)

        def hanoi(disk, start=_start, end=_spare, middle=_dest):
            if disk > 0:
                hanoi(disk - 1, start, middle, end)
                move(self, start[0], end[0], -1)
                import time
                time.sleep(1)
                hanoi(disk - 1, middle, end, start)

        def solve_hanoi(n=self.numcards, start=_start, dest=_dest, spare=_spare):

            if n == 1:
                if len(_dest[1]) == 1:
                    pass#print "done"
                else:
                    if len(_start[1]) == 1:
                        hanoi(1, _start, _dest, _spare)
                    else:
                        hanoi(1, _spare, _dest, _start)
            elif n > 1:
                i = 1
                j = 2
                while i < n and j <= n:
                    start = ""
                    for tower in [_start, _spare, _dest]:
                        for t in tower[1]:
                            if i == t.rank:
                                start = tower
                                break
                        if start != "":
                            break
                    if start == "":
                        continue
                    else:
                        while j <= n:
                            dest = ""
                            for tower1 in [_start, _spare, _dest]:
                                for t in tower1[1]:
                                    if j == t.rank:
                                        if tower1[0] == start[0]:
                                            j += 1
                                            break
                                        else:
                                            dest = tower1
                                            for pole in [_start, _spare, _dest]:
                                                if pole[0] != start[0] and pole[0] != dest[0]:
                                                    spare = pole
                                if tower1[0] == start[0]:
                                    break
                            if dest != "" or (j == n and tower1[0] == start[0]):
                                if j != n:
                                    hanoi(j, start, dest, spare)
                                    start = []
                                    for each in dest:
                                        start.append(each)
                                if j == n:
                                    if start[0] == "start":
                                        hanoi(j, _start, _dest, _spare)
                                    elif start[0] == "spare":
                                        hanoi(j, _spare, _dest, _start)
                                    else:
                                        #print "Tower of Hanoi Complete"
                                        break
                                j += 1
                    if j == n:
                        if start[0] == "start":
                            hanoi(j, _start, _dest, _spare)
                        elif start[0] == "spare":
                            hanoi(j, _spare, _dest, _start)
                        else:
                            #print "Tower of Hanoi Complete"
                            break
        solve_hanoi()

    def update(self):
        return self.check_win()

    def check_win(self):
        if len(self.stacks[2].cards) < self.numcards:
            return False
        return True

    def bindings(self):
        """Define mouse bindings for game"""
        return self._bindings.value()

    def deal(self):
        """No in-game deals present in Hanoi games"""
        pass


class Hanoi3(Hanoi):
    name = "Hanoi3"

    def __init__(self, num_cards=3):
        super(Hanoi3, self).__init__(num_cards=num_cards)


class Hanoi5(Hanoi):
    name = "Hanoi5"

    def __init__(self, num_cards=5):
        super(Hanoi5, self).__init__(num_cards=num_cards)

DB.add_game("Hanoi3", Hanoi3)
DB.add_game("Hanoi4", Hanoi)
DB.add_game("Hanoi5", Hanoi5)
