class Action:
    def __init__(self, moment, action, value, number):
        self._moment = moment
        self._action = action
        self._value = value
        self._number = number

    @property
    def moment(self):
        return self._moment

    @property
    def action(self):
        return self._action

    @property
    def value(self):
        return self._value

    @property
    def number(self):
        return self._number

    def __str__(self):
        return f'''{self.moment}, {self.action}, {self.value} '''
