import json
import sys

from colorama import Fore, Style
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
# noinspection DuplicatedCode
from Card import Card
from Hand import Hand

Builder.load_file('gui.kv')


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
    def actionMoment(self, moment: str):
        self._actionMoment = moment

    def verifyPlayers(self):
        print('Players in the hand : ')
        players = self.playedHand.players
        for player in players:
            print(player.name)
        while True:
            user = input('What is your username ? ')
            for player in players:
                if player.name == user:
                    print('Hello ', user)
                    return user
            print('Username not found, please try again')

    def createTable(self, username: str, nextInput: str):
        if nextInput == '+':
            self.actionNumber = self.actionNumber + 1
            self._nextAction = '+'
        else:
            if self.actionNumber == 0:
                raise Exception('First action')
            self.actionNumber = self.actionNumber - 1
            self._nextAction = '-'

        organized_players = self.playedHand.organizeData(username)
        cards = organized_players[0].hand
        names, actions = self.actions(organized_players)
        board = self.showCards()
        button = self.playerButton()
        stack = [player.stack for player in self.playedHand.players]

        if self.actionMoment == 'end':
            names, actions = self.results(names)

        return names, actions, button, cards, stack, board

    def printHandFullRing(self, names: list, actions: list, button: list, cards: list, stack: list, board: list):

        tableString = f'''
({names[3]})          ({names[4]})           ({names[5]})           ({names[6]})
    {stack[3]:^9}    __________    {stack[4]:^9}    ___________    {stack[5]:^9}    ___________    {stack[6]:^9} 
            /  {actions[3]}    {actions[4]}  {button[4]}                {actions[5]}  {button[5]}        {actions[6]} \\
           /  {button[3]}                _____   _____   _____    _____   _____                {button[6]} \\
          /                   |     | |     | |     |  |     | |     |                  \\
          |   {button[2]}               |  {board[0].number}  | |  {board[1].number}  | |  {board[2].number}  |  \
|  {board[3].number}  | |  {board[4].number}  |               {button[7]}   | 
({names[2]}) {actions[2]}   |  {board[0].color}  | |  {board[1].color}  | |  {board[2].color}  |  |  {board[3].color} \
 | |  {board[4].color}  |  {actions[7]} ({names[7]})
    {stack[2]:^9}                 |_____| |_____| |_____|  |_____| |_____|	               {stack[7]:^9}
          |                                                                              |
          \\                              POT : {self.playedHand.pot:^9}                                /
           \\  {button[1]}                                                                     {button[8]}  /
            \\  {actions[1]}                  {button[0]}  {actions[0]}                     {actions[8]}  /
({names[1]})________________________({names[0]})________________________({names[8]})
    {stack[1]:^9} 	                             {stack[0]:^9}                                {stack[8]:^9}
                                          _____    _____
                                         |     |  |     |
                                         |  {cards[0].number}  |  |  {cards[1].number}  |
                                         |  {cards[0].color}  |  |  {cards[1].color}  |
                                         |_____|  |_____|
        '''

        print(tableString)

    def actions(self, players: list):
        if self._nextAction == '-':
            for action in self._lastAction:
                if action != '         ' and action != '  fold  ':
                    self.playedHand.pot = self.playedHand.pot - int(action[1:])
                    self.playedHand.players[self._lastAction.index(action)].stack = \
                        self.playedHand.players[self._lastAction.index(action)].stack + int(action[1:])

        playerNames = [f"{player.name:^15}" for player in self.playedHand.players]
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
                    handActions.append('  fold  ')
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

    def playerButton(self):
        positions = []
        for player in self.playedHand.players:
            positions.append('@') if player.position == 'button' else positions.append(' ')
        return positions

    def results(self, names: list):
        actions = []
        for player in self.playedHand.players:
            if player.result > 0:
                playerName = f'{player.name:^15}'
                names[names.index(playerName)] = f'{Fore.YELLOW}{playerName}{Style.RESET_ALL}'
                actions.append(f'+{player.result:^8}')
                print(player)
            else:
                actions.append('         ')
        self.playedHand.pot = 0
        return names, actions


class MyApp(Widget):
    username = ''
    names, actions, button, cards, stack, board = [], [], [], [], [], []
    player = 0

    def setValues(self):
        return [player.name for player in hand.playedHand.players]

    def spinner_clicked(self, value):
        pass

    def submit_user(self, username):
        self.username = username
        self.ids.username_label.text = f'{username}'
        names, actions, button, cards, stack, board = hand.createTable(self.username, '+')
        self.ids.player1.text = f'{names[0]} {actions[0]}'
        self.ids.player2.text = f'{names[1]} {actions[1]}'
        self.ids.player3.text = f'{names[2]} {actions[2]}'
        self.ids.player4.text = f'{names[3]} {actions[3]}'
        self.ids.player5.text = f'{names[4]} {actions[4]}'
        self.ids.player6.text = f'{names[5]} {actions[5]}'
        self.ids.player7.text = f'{names[6]} {actions[6]}'
        self.ids.player8.text = f'{names[7]} {actions[7]}'
        self.ids.player9.text = f'{names[8]} {actions[8]}'

        self.ids.flop1.text = f'{board[0]} '
        self.ids.flop2.text = f'{board[1]} '
        self.ids.flop3.text = f'{board[2]} '
        self.ids.turn.text = f'{board[3]} '
        self.ids.river.text = f'{board[4]} '

        self.ids.submit.disabled = True

    def show_username(self):
        return self.username

    def next(self):
        names, actions, button, cards, stack, board = hand.createTable(self.username, '+')
        self.ids.player1.text = f'{names[0]} {actions[0]}'
        self.ids.player2.text = f'{names[1]} {actions[1]}'
        self.ids.player3.text = f'{names[2]} {actions[2]}'
        self.ids.player4.text = f'{names[3]} {actions[3]}'
        self.ids.player5.text = f'{names[4]} {actions[4]}'
        self.ids.player6.text = f'{names[5]} {actions[5]}'
        self.ids.player7.text = f'{names[6]} {actions[6]}'
        self.ids.player8.text = f'{names[7]} {actions[7]}'
        self.ids.player9.text = f'{names[8]} {actions[8]}'

        self.ids.flop1.text = f'{board[0]} '
        self.ids.flop2.text = f'{board[1]} '
        self.ids.flop3.text = f'{board[2]} '
        self.ids.turn.text = f'{board[3]} '
        self.ids.river.text = f'{board[4]} '

    def previous(self):
        names, actions, button, cards, stack, board = hand.createTable(self.username, '-')
        self.ids.player1.text = f'{names[0]} {actions[0]}'
        self.ids.player2.text = f'{names[1]} {actions[1]}'
        self.ids.player3.text = f'{names[2]} {actions[2]}'
        self.ids.player4.text = f'{names[3]} {actions[3]}'
        self.ids.player5.text = f'{names[4]} {actions[4]}'
        self.ids.player6.text = f'{names[5]} {actions[5]}'
        self.ids.player7.text = f'{names[6]} {actions[6]}'
        self.ids.player8.text = f'{names[7]} {actions[7]}'
        self.ids.player9.text = f'{names[8]} {actions[8]}'

        self.ids.flop1.text = f'{board[0]} '
        self.ids.flop2.text = f'{board[1]} '
        self.ids.flop3.text = f'{board[2]} '
        self.ids.turn.text = f'{board[3]} '
        self.ids.river.text = f'{board[4]} '


class UserApp(App):

    def build(self):
        return MyApp()


if __name__ == '__main__':
    with open(sys.argv[1]) as json_file:
        data = json.load(json_file)
        handPot = data["hand"]['pot']
        handPlayers = data["hand"]["players"]
        handCards = data["hand"]["board"]

    hand = Runner(handPot, handPlayers, handCards)
    if sys.argv[2] == "gui":
        UserApp().run()
    else:
        handUser = hand.verifyPlayers()

        names, actions, button, cards, stack, board = hand.createTable(handUser, '+')
        hand.printHandFullRing(names, actions, button, cards, stack, board)

        while True:
            stop = ''
            if hand.actionMoment == 'end':
                print('Hand review ended.')
                break
            value = input('Press + to go to next step or - to go back to last step or enter to quit: ')
            if value == '+':
                names, actions, button, cards, stack, board = hand.createTable(handUser, '+')
                hand.printHandFullRing(names, actions, button, cards, stack, board)
            elif value == '-':
                names, actions, button, cards, stack, board = hand.createTable(handUser, '-')
                hand.printHandFullRing(names, actions, button, cards, stack, board)
            elif value == '':
                while stop != 'Y' or 'y' or 'N' or 'n':
                    stop = input('Are you sure you want to quit ? Y/N ')
                    if stop == 'Y' or 'y' or 'N' or 'n':
                        break
            if stop == 'Y' or stop == 'y':
                break
