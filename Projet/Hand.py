from .Player import Player
from .Card import Card


class Hand:
    def __init__(self, pot, players, cards):
        self._players = []
        self._pot = pot
        self._board = []
        if len(players) > 0:
            for player in players:
                self._players.append(
                    Player(player['name'], player['stack'], player['position'], player['actions'], player['result'],
                           player['status'], player['hand']))
        if len(cards) > 0:
            for card in cards:
                self._board.append(Card(card['value'], card['color']))

    @property
    def players(self):
        return self._players

    @property
    def pot(self):
        return self._pot

    @property
    def board(self):
        return self._board

    @pot.setter
    def pot(self, value):
        self._pot = value

    def verifyPlayers(self, userName):
        for player in self.players:
            print(player.name())
            if player.name == userName:
                return True
        return False

    def organizeData(self, username: str):
        players = self.players
        playernames = [player.name for player in players]
        while playernames[0] != username:
            players.append(players.pop(0))
            playernames.append(playernames.pop(0))
        names = []
        for name in playernames:
            name = f"{name:^15}"
            names.append(name)
        return players, names
