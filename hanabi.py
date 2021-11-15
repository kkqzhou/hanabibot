import numpy as np

import random
from typing import Dict, Iterable, List, Tuple
from card import Card
from player import Player, Hint, Play, Discard

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

        self.history = []
        self.played = [Card(i, 0) for i in range(NUM_COLORS)]
        self.discarded = []
        self.strikes = 0
        self.hints = 8


    def shuffle_cards(self) -> List[Card]:
        deck = []
        for i in range(NUM_COLORS):
            deck.extend([Card(i, 1)] * 3 + [Card(i, 2)] * 2 + [Card(i, 3)] * 2 + [Card(i, 4)] * 2 + [Card(i, 5)])
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

    def draw_new_card(self, player_num: int, card_idx: int) -> bool:
        cards = self.player_cards[player_num]
        # Count played/discarded both as discarded
        self.discarded.append(cards[card_idx])
        del cards[card_idx]
        new_card = None
        if self.deck:
            new_card = self.deck.pop()
        if not new_card:
            return False
        cards.append(new_card)
        return True

    def play_card(self, card: Card) -> bool:
        idx_played_to = card.color
        last_played = self.played[idx_played_to]
        if last_played.number == card.number - 1:
            last_played.number += 1
            return True
        return False

    def play_complete(self) -> int:
        done = False
        counting_down_out_of_cards = False
        count_down_out_of_cards = 0

        while not done:
            for i, player in enumerate(self.players):
                visible_hands = {
                    j: player_cards for j, player_cards in self.player_cards.items() if i != j
                }
                new_action = player.play(i,
                    visible_hands,
                    self.played,
                    self.discarded,
                    self.history,
                    self.hints,
                    self.strikes
                )
                self.history.append(new_action)
                remaining_cards = True
                if isinstance(new_action, Play):
                    idx = new_action.idx
                    card = self.player_cards[i][idx]
                    new_action.card = card
                    if self.play_card(card):
                        new_action.success = True
                    else:
                        new_action.success = False
                        self.strikes += 1
                    remaining_cards = self.draw_new_card(i, idx)
                elif isinstance(new_action, Hint):
                    self.hints -= 1
                elif isinstance(new_action, Discard):
                    idx = new_action.idx
                    card = self.player_cards[i][idx]
                    new_action.card = card
                    self.hints += 1
                    remaining_cards = self.draw_new_card(i, idx)
                    
                if not remaining_cards and not counting_down_out_of_cards:
                    counting_down_out_of_cards = True
                    count_down_out_of_cards = self.num_players

                if self.strikes >= 3:
                    done = True
                    print("Structed out")
                    break

                if counting_down_out_of_cards:
                    count_down_out_of_cards -= 1
                    if not count_down_out_of_cards:
                        done = True
                        break




if __name__ == '__main__':
    np.random.seed(123456789)
    from dumb_player import DumbPlayer
    game = HanabiGame(players=[DumbPlayer() for _ in range(4)])
    print(game.player_cards)
    print(len(game.deck))
    print(game.deck)
    print(game.play_complete())
