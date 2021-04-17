from .Action import Action
from .Card import Card


class Player:
    def __init__(self, name, stack, position, actions, result, status=True, cards=None):
        self._hand = []
        self._name = name
        self._stack = stack
        self._position = position
        self._status = status
        if cards is not None:
            for card in cards:
                self._hand.append(Card(card['value'], card['color']))
        self._actions = []
        for action in actions:
            self._actions.append(Action(action['moment'], action['type'], action['value'], action['id']))
        self._result = result

    @property
    def name(self):
        return self._name

    @property
    def stack(self):
        return self._stack

    @stack.setter
    def stack(self, value):
        self._stack = value

    @property
    def actions(self):
        return self._actions

    @property
    def hand(self):
        return self._hand

    @property
    def position(self):
        return self._position

    @property
    def result(self):
        return self._result
