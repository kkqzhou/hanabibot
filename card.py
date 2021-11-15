class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number

    def __repr__(self):
        return ("Card{%s, %s}" % (self.color, self.number))

