from Player import Player
from Card import Card


class Hand:
    def __init__(self, pot: int, players: [Player], cards: [Card]):
        """This builds a hand with players, a pot value and cards on the board.

        PRE : [int] pot : valeur du pot au début de la main
              [List of Player] players : all players present in the hand
              [List of Card] cards : cards to display on the poker table
        POST : Create a new hand of poker
        """
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

    def verifyPlayers(self, user: str):
        """This method checks if user is present in the hand

        PRE : [str] user : username of the player using the app
        POST : [Boolean] Returns True if the username was found in the list of players
                         Returns False if the username was not found in the list of players
        """
        for player in self.players:
            if player.name == user:
                return True
        return False

    def organizeData(self, username: str):
        """This method changes the order of the players to set the user as first

        PRE : [str] user : username of the player using the app
        POST : [List of Player] Returns the reordered list of players in hand
        """
        players = self.players
        playerNames = [player.name for player in players]
        while playerNames[0] != username:
            players.append(players.pop(0))
            playerNames.append(playerNames.pop(0))
        return players
