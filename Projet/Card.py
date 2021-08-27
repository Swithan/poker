class Card:
    def __init__(self, number, color):
        self._number = number
        self._color = color

    @property
    def color(self):
        return self._color

    @property
    def number(self):
        return self._number

    def __str__(self):
        return f'''
 _____
|     |
|  {self.number}  |
|  {self.color}  |
|_____|
'''
