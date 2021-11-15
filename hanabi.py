import numpy as np

import random
from typing import Dict, Iterable, List, Tuple
from card import Card
from player import Player

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
NUM_COLORS = 6

class HanabiGame:
    def __init__(self, players: List[Player]):
        self.num_players = len(players)
        self.deck: List[Card] = self.shuffle_cards()
        self.player_cards, self.deck = self.deal_cards(self.deck)
        self.players = players
        self.strikes = 0
        self.hints = 8

    def shuffle_cards(self) -> List[Card]:
        deck = []
        for i in range(NUM_COLORS):
            for j in range(1,6):
                count = 1
                if j == 1:
                    count = 3
                if j < 5:
                    count = 2
                deck.append(Card(i, j))
        random.shuffle(deck)
        return deck

    def deal_cards(self, deck: List[Card]) -> Tuple[Dict[int, List[Card]], List[Card]]:
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

    def play_complete(self):
        history = []
        played = [Card(i, 0) for i in range(NUM_COLORS)]
        discarded = []
        for i, player in enumerate(self.players):
            visible_hands = {
                j: player_cards for j, player_cards in self.player_cards.items() if i != j
            }
            new_action = player.play(i, visible_hands, played, discarded, history)
            history.append(new_action)
            # TBD: Check strikes/hints/played
        

if __name__ == '__main__':
    np.random.seed(123456789)
    game = HanabiGame(players=[1,2,3,4])
    print(game.player_cards)
    print(len(game.deck))
    print(game.deck)
