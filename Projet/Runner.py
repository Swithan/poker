import json

from colorama import Fore, Style

from Projet.Card import Card
from Projet.Hand import Hand


class Runner:

    def __init__(self, pot, players, cards):
        self._nextAction = '+'
        self._lastAction = []
        self._actionNumber = 0
        self._actionMoment = 'preflop'
        self._playedHand = Hand(pot, players, cards)

    @property
    def playedHand(self):
        return self._playedHand

    @property
    def actionNumber(self):
        return self._actionNumber

    @actionNumber.setter
    def actionNumber(self, number):
        self._actionNumber = number

    @property
    def actionMoment(self):
        return self._actionMoment

    @actionMoment.setter
    def actionMoment(self, moment):
        self._actionMoment = moment

    def verifyPlayers(self):
        hand = self.playedHand
        print('Players in the hand : ')
        players = hand.players
        for player in players:
            print(player.name)
        while True:
            user = input('What is your username ? ')
            for player in players:
                if player.name == user:
                    print('Hello ', user)
                    return user
            print('Username not found, please try again')

    def createTable(self, username, nextInput):
        # TODO : check action called
        # if action = nextStep:
        #       lastAction = actual action
        #       actual action = build new action
        #       new action: verify if action + 1 = show cards
        if nextInput == '+':
            self.actionNumber = self.actionNumber + 1
            self._nextAction = '+'
        else:
            self.actionNumber = self.actionNumber - 1
            self._nextAction = '-'
        hand = self.playedHand
        count = len(hand.players)
        if count == 9:
            self.printHandFullRing(username)
        elif count > 2:
            self.printHandSixMax(username)
        else:
            self.printHandHeadsUp(username)

    def printHandHeadsUp(self, username):
        table = [
            '              ____________________( xxxxxx )________________________',
            '             /                       xxxx                          \\',
            '            /                     (B) + $$$$                        \\',
            '           /          _____   _____   _____    _____   _____         \\',
            '          /          |     | |     | |     |  |     | |     |         \\',
            '          |          |  X  | |  X  | |  X  |  |  X  | |  X  |          |',
            '          |          |  X  | |  X  | |  X  |  |  X  | |  X  |          |',
            '          |          |_____| |_____| |_____|  |_____| |_____|	        |',
            '          |                                                            |',
            '          \                     POT : XXXXXX                          /',
            '           \                                                         /',
            '            \                     (B) + $$$$                        /',
            '             \____________________( xxxxxx )_______________________/',
            '                			          xxxx		                   ',
            '                                 _____    _____',
            '                                |     |  |     |',
            '                                |  X  |  |  X  |',
            '                                |  X  |  |  X  |',
            '                                |_____|  |_____|'
        ]
        for line in table:
            print(line)

    def printHandSixMax(self, username):
        table = [
            '          ( XXXXX )                ( XXXXX )                 ( XXXXX )',
            '             xxx   ________________   xxx   _________________   xxx',
            '            /    + $$$            (B) + $$$                + $$$    \\',
            '           /  (B)     _____   _____   _____    _____   _____     (B) \\',
            '          /          |     | |     | |     |  |     | |     |         \\',
            '          |          |  X  | |  X  | |  X  |  |  X  | |  X  |          |',
            '          |          |  X  | |  X  | |  X  |  |  X  | |  X  |          |',
            '          |          |_____| |_____| |_____|  |_____| |_____|	        |',
            '          |                                                            |',
            '          \                     POT : XXXXXX                          /',
            '           \ (B)                                                (B)  /',
            '            \   + $$$             (B) + $$$                + $$$    /',
            '          ( xxxxx )________________( xxxxxx )________________( xxxxx )',
            '             xxx			           xxxx		                 xxx',
            '                                 _____    _____',
            '                                |     |  |     |',
            '                                |  X  |  |  X  |',
            '                                |  X  |  |  X  |',
            '                                |_____|  |_____|'
        ]
        for line in table:
            print(line)

    def printHandFullRing(self, username):
        data, names = self.playedHand.organizeData(username)
        playerCards = data[0].hand
        names, actions = self.actions(data, names)
        cards = self.showCards()
        button = self.playerButton(data)

        if self.actionMoment == 'end':
            names, actions = self.results(names)

        tableString = f'''
({names[3]})          ({names[4]})           ({names[5]})           ({names[6]})
    {data[3].stack:^9}    __________    {data[4].stack:^9}    ___________    {data[5].stack:^9}    ___________    {data[6].stack:^9} 
            /  {actions[3]}    {actions[4]}  {button[4]}                {actions[5]}  {button[5]}        {actions[6]} \\
           /  {button[3]}                _____   _____   _____    _____   _____                {button[6]} \\
          /                   |     | |     | |     |  |     | |     |                  \\
          |   {button[2]}               |  {cards[0].number}  | |  {cards[1].number}  | |  {cards[2].number}  |  |  {cards[3].number}  | |  {cards[4].number}  |               {button[7]}   | 
({names[2]}) {actions[2]}   |  {cards[0].color}  | |  {cards[1].color}  | |  {cards[2].color}  |  |  {cards[3].color}  | |  {cards[4].color}  |  {actions[7]} ({names[7]})
    {data[2].stack:^9}                 |_____| |_____| |_____|  |_____| |_____|	               {data[7].stack:^9}
          |                                                                              |
          \                              POT : {self.playedHand.pot:^9}                                /
           \  {button[1]}                                                                     {button[8]}  /
            \  {actions[1]}                  {button[0]}  {actions[0]}                     {actions[8]}  /
({names[1]})________________________({names[0]})________________________({names[8]})
    {data[1].stack:^9} 	                             {data[0].stack:^9}                                {data[8].stack:^9}
                                          _____    _____
                                         |     |  |     |
                                         |  {playerCards[0].number}  |  |  {playerCards[1].number}  |
                                         |  {playerCards[0].color}  |  |  {playerCards[1].color}  |
                                         |_____|  |_____|'
        '''

        print(tableString)

    def actions(self, players, names):
        if self._nextAction == '-':
            for action in self._lastAction:
                if action != '         ':
                    self.playedHand.pot = self.playedHand.pot - int(action[1:])
                    self.playedHand.players[self._lastAction.index(action)].stack = \
                        self.playedHand.players[self._lastAction.index(action)].stack + int(action[1:])
        playerNames = names
        handActions = []
        actionMade = False
        for player in players:
            actions = player.actions
            added = False
            for action in actions:
                if action.number == self.actionNumber and action.action != 'fold':
                    handActions.append(f'+{action.value:^8}')
                    if self._nextAction != '-':
                        self.playedHand.pot = self.playedHand.pot + action.value
                        player.stack = player.stack - action.value
                    playerNames[players.index(player)] = \
                        f'{Fore.CYAN}{playerNames[players.index(player)]}{Style.RESET_ALL}'
                    actionMade = True
                    added = True
                elif action.number == self.actionNumber and action.action == 'fold':
                    actionMade = True
                elif (action.number == self.actionNumber or action.number < self.actionNumber) \
                        and action.action == 'fold':
                    playerNames[players.index(player)] = \
                        f'{Fore.LIGHTBLACK_EX}{playerNames[players.index(player)]}{Style.RESET_ALL}'
            if not added:
                handActions.append('         ')
        if not actionMade:
            if self.actionMoment == 'preflop':
                self.actionMoment = 'flop'
            elif self.actionMoment == 'flop':
                self.actionMoment = 'turn'
            elif self.actionMoment == 'turn':
                self.actionMoment = 'river'
            elif self.actionMoment == 'river':
                self.actionMoment = 'end'
        self._lastAction = handActions
        return playerNames, handActions

    def showCards(self):
        board = [card for card in self.playedHand.board]
        emptyCard = Card(' ', ' ')
        if self.actionMoment == 'preflop':
            board = [emptyCard, emptyCard, emptyCard, emptyCard, emptyCard]
        if self.actionMoment == 'flop':
            board = board[:3]
            board.append(emptyCard)
            board.append(emptyCard)
        elif self.actionMoment == 'turn':
            board = board[:4]
            board.append(emptyCard)
        return board

    def playerButton(self, players):
        positions = []
        for player in players:
            if player.position == 'button':
                positions.append('@')
            else:
                positions.append(' ')
        return positions

    def results(self, names):
        playerNames = names
        actions = []
        for player in self.playedHand.players:
            if player.result > 0:
                playerName = f'{player.name:^15}'
                playerNames[playerNames.index(playerName)] = f'{Fore.YELLOW}{playerName}{Style.RESET_ALL}'
                actions.append(f'+{player.result:^8}')
            else:
                actions.append('         ')
        self.playedHand.pot = 0
        return names, actions


if __name__ == '__main__':
    with open("hands.json") as json_file:
        data = json.load(json_file)
        pot = data["hand"]['pot']
        players = data["hand"]["players"]
        cards = data["hand"]["board"]

    hand = Runner(pot, players, cards)

    username = hand.verifyPlayers()

    hand.createTable(username, '+')
    while True:
        stop = ''
        if hand.actionMoment == 'end':
            print('Hand review ended.')
            break
        value = input('Press + to go to next step or - to go back to last step or enter to quit: ')
        if value == '+':
            hand.createTable(username, '+')
        elif value == '-':
            hand.createTable(username, '-')
        elif value == '':
            while stop != 'Y' or 'y' or 'N' or 'n':
                stop = input('Are you sure you want to quit ? Y/N ')
                if stop == 'Y' or 'y':
                    break
                elif stop == 'N' or 'n':
                    break
        if stop == 'Y' or stop == 'y':
            break
