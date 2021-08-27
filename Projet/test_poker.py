import unittest
from Action import Action
from Hand import Hand
from Player import Player
from Runner import Runner
from Card import Card
import mock

class action(unittest.TestCase):
    def test_action_string(self):
        self.assertEqual(str(Action('flop', 'fold', 0, 1)), 'flop, fold, 0 ')


testCards = [{'color': 'd', 'value': '9'}, {'color': 's', 'value': '8'}, {'color': 'h', 'value': '9'}, {'color': 'd', 'value': '2'}, {'color': 'c', 'value': '2'}]

players = [{'name': 'Swithan', 'stack': 1500, 'position': 'LJ', 'status': True, 'hand': [{'color': 'h', 'value': 'A'}, {'color': 's', 'value': 'K'}], 'actions': [{'id': 6, 'moment': 'preflop', 'type': 'raise', 'value': 70}, {'id': 12, 'moment': 'preflop', 'type': 'call All-In', 'value': 1430}], 'result': -1500}]
players2 = [{'name': 'PlumbBobcat', 'stack': 1500, 'position': 'button', 'status': True, 'hand': [], 'actions': [{'id': 9, 'moment': 'preflop', 'type': 'fold', 'value': 0}], 'result': 0}, {'name': 'perepeppepe', 'stack': 1500, 'position': 'small blind', 'status': True, 'hand': [], 'actions': [{'id': 1, 'moment': 'preflop', 'type': 'sb', 'value': 10}, {'id': 10, 'moment': 'preflop', 'type': 'fold', 'value': 0}], 'result': -10}, {'name': 'HoneyBuns96', 'stack': 1500, 'position': 'big blind', 'status': True, 'hand': [], 'actions': [{'id': 2, 'moment': 'preflop', 'type': 'bb', 'value': 20}, {'id': 11, 'moment': 'preflop', 'type': 'fold', 'value': 0}], 'result': -20}, {'name': '2Legit1900', 'stack': 1500, 'position': 'UTG', 'status': False, 'hand': [], 'actions': [{'id': 3, 'moment': 'preflop', 'type': 'fold', 'value': 0}], 'result': 0}, {'name': 'looper549', 'stack': 1500, 'position': 'UTG+1', 'status': True, 'hand': [], 'actions': [{'id': 4, 'moment': 'preflop', 'type': 'fold', 'value': 0}], 'result': 0}, {'name': 'badgdj', 'stack': 1500, 'position': 'MP', 'status': True, 'hand': [], 'actions': [{'id': 5, 'moment': 'preflop', 'type': 'fold', 'value': 0}], 'result': 0}, {'name': 'Swithan', 'stack': 1500, 'position': 'LJ', 'status': True, 'hand': [{'color': 'h', 'value': 'A'}, {'color': 's', 'value': 'K'}], 'actions': [{'id': 6, 'moment': 'preflop', 'type': 'raise', 'value': 70}, {'id': 12, 'moment': 'preflop', 'type': 'call All-In', 'value': 1430}], 'result': -1500}, {'name': 'sergej275', 'stack': 1500, 'position': 'HJ', 'status': True, 'hand': [], 'actions': [{'id': 7, 'moment': 'preflop', 'type': 'call', 'value': 70}, {'id': 13, 'moment': 'preflop', 'type': 'fold', 'value': 0}], 'result': -70}, {'name': 'UnCrownedKings', 'stack': 1500, 'position': 'CO', 'status': True, 'hand': [], 'actions': [{'id': 8, 'moment': 'preflop', 'type': 'raise All-In', 'value': 1500}], 'result': 3100}]

testHand = Hand(pot=0, players=players, cards=[{'color': 'd', 'value': '9'}, {'color': 's', 'value': '8'}, {'color': 'h', 'value': '9'}, {'color': 'd', 'value': '2'}, {'color': 'c', 'value': '2'}])
testHand2 = Hand(pot=0, players=players2, cards=[{'color': 'd', 'value': '9'}, {'color': 's', 'value': '8'}, {'color': 'h', 'value': '9'}, {'color': 'd', 'value': '2'}, {'color': 'c', 'value': '2'}])

testRunner = Runner(cards=testCards, players=players2, pot=0)

class cards(unittest.TestCase):
    def test_cards_string(self):
        self.assertEqual(str(Card(color='Pique', number='As')), '''
 _____
|     |
|  As  |
|  Pique  |
|_____|
''')


class hand(unittest.TestCase):
    def test_verifyPlayers(self):
        self.assertEqual(testHand.verifyPlayers('Swithan'), True)
        self.assertEqual(testHand.verifyPlayers('Personne'), False)

    def test_organizeData(self):
        self.assertEqual(testHand.organizeData('Swithan')[0].name, [Player('Swithan', 1500, 'LJ', [{'id': 6, 'moment': 'preflop', 'type': 'raise', 'value': 70}, {'id': 12, 'moment': 'preflop', 'type': 'call All-In', 'value': 1430}], -1500, True, [{'color': 'h', 'value': 'A'}, {'color': 's', 'value': 'K'}])][0].name)
        self.assertEqual(testHand2.organizeData('Swithan')[0].name, [Player('Swithan', 1500, 'LJ', [{'id': 6, 'moment': 'preflop', 'type': 'raise', 'value': 70}, {'id': 12, 'moment': 'preflop', 'type': 'call All-In', 'value': 1430}], -1500, True, [{'color': 'h', 'value': 'A'}, {'color': 's', 'value': 'K'}])][0].name)
        self.assertEqual(testHand2.organizeData('Swithan')[1].name, [Player('sergej275', 1500, 'HJ', [{'id': 7, 'moment': 'preflop', 'type': 'call', 'value': 70}, {'id': 13, 'moment': 'preflop', 'type': 'fold', 'value': 0}], -70, True, [])][0].name)


class runner(unittest.TestCase):
    def test_verifyPlayers(self):
        with mock.patch('builtins.input', return_value="Swithan"):
            assert Runner(cards=testCards, players=players2, pot=0).verifyPlayers() == "Swithan"

    def test_createTable(self):
        self.assertEqual(testRunner.createTable('Swithan', '+')[0][0], '    Swithan    ')  # player name
        self.assertEqual(testRunner.createTable('Swithan', '+')[1][0], '         ')  # player not doing action
        testRunner.createTable('Swithan', '-')
        self.assertEqual(testRunner.createTable('Swithan', '+')[2][0], ' ')  # player not button
        testRunner.createTable('Swithan', '-')
        self.assertEqual(testRunner.createTable('Swithan', '+')[3][0].color, 'h')  # player has heart card
        testRunner.createTable('Swithan', '-')
        self.assertEqual(testRunner.createTable('Swithan', '+')[3][0].number, 'A')  # player has Ace card
        testRunner.createTable('Swithan', '-')
        self.assertEqual(testRunner.createTable('Swithan', '+')[4][0], 1500)  # player has Ace card
        # go to flop cards
        testRunner.createTable('Swithan', '+')
        testRunner.createTable('Swithan', '+')
        testRunner.createTable('Swithan', '+')
        testRunner.createTable('Swithan', '+')
        testRunner.createTable('Swithan', '+')
        testRunner.createTable('Swithan', '+')
        testRunner.createTable('Swithan', '+')
        testRunner.createTable('Swithan', '+')
        testRunner.createTable('Swithan', '+')
        testRunner.createTable('Swithan', '+')
        testRunner.createTable('Swithan', '+')
        self.assertEqual(testRunner.createTable('Swithan', '+')[5][0].color, 'd')  # player has Ace card
        testRunner.createTable('Swithan', '-')
        self.assertEqual(testRunner.createTable('Swithan', '+')[5][0].number, '9')  # player has Ace card
        testRunner.createTable('Swithan', '-')
