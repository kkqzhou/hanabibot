import numpy as np

from typing import Dict, Iterable, List, Tuple

"""
Game rules for the card game Hanabi are encoded here. The standard setup of the game involves 60 Hanabi cards, 
8 Hint tokens, and 3 Misplay tokens. The Hanabi cards are distributed as follows:

Six colors: rainbow, red, yellow, green, blue, white
10 cards per color: 1, 1, 1, 2, 2, 3, 3, 4, 4, 5.

With 2-3 players, each player starts with 5 cards in hand.
With 4-5 players, each player starts with 4 cards in hand.

Representations:
* Card: int - 0..59
* Color: The tens digit of each card mapped as follows - {0: rainbow, 1: red, 2: yellow, 3: green, 4: blue, 5: white}
* Number: The units digit of each card mapped as follows - {0: 1, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 5}
"""

TOTAL_NUM_CARDS = 60

def card_to_color(card: int) -> int:
    return card // 10

def card_to_number(card: int) -> int:
    return {0: 1, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 5}[card % 10]

class HanabiGame:
    def __init__(self, num_players: int):
        self.num_players = num_players
        self.deck: Iterable[int] = self.shuffle_cards()
        self.player_cards, self.deck = self.deal_cards(self.deck)

    def shuffle_cards(self) -> Iterable[int]:
        return np.random.permutation(TOTAL_NUM_CARDS)

    def deal_cards(self, deck: Iterable[int]) -> Tuple[Dict[int, Iterable[int]], Iterable[int]]:
        if self.num_players in {2, 3}:
            player_cards = {i: deck[i*5:(i+1)*5] for i in range(self.num_players)}
            deck = deck[self.num_players*5:]
            return player_cards, deck
        elif self.num_players in {4, 5}:
            player_cards = {i: deck[i*4:(i+1)*4] for i in range(self.num_players)}
            deck = deck[self.num_players*4:]
            return player_cards, deck
        else:
            raise NotImplementedError

if __name__ == '__main__':
    np.random.seed(123456789)
    game = HanabiGame(num_players=4)
    print(game.player_cards)
    print(len(game.deck))
    print(game.deck)