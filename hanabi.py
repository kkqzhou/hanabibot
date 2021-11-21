import numpy as np

import random
from action import Hint, HintType, Play, Discard, INT_TO_COLOR_REPR
from typing import Dict, Iterable, List, Tuple
from card import Card
from player import Player

import tabulate

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
    def __init__(self, players: List[Player], verbose: bool = False):
        self.verbose = verbose
        self.players = players
        self.num_players = len(players)
        self.deck: List[Card] = self.shuffle_cards()
        self.player_cards, self.deck = self.deal_cards(self.deck)

        self.history = []
        self.played = [Card(i, 0, []) for i in range(NUM_COLORS)]
        self.discarded = []
        self.strikes = 0
        self.num_hints = 8

    def print_game_state(self):
        raw_cards_strs = [f"P{player}: [{' '.join([str(card) for card in cards])}]" for player, cards in self.player_cards.items()]
        raw_hints_strs = []
        for player, cards in self.player_cards.items():
            raw_hints_str = f"     "
            for card in cards:
                number_hints = [hint for hint in card.hints if hint.hint_type == HintType.NUMBER]
                color_hints = [hint for hint in card.hints if hint.hint_type == HintType.COLOR]
                raw_hints_str += str(number_hints[0].hint_value) if len(number_hints) else " "
                raw_hints_str += INT_TO_COLOR_REPR[color_hints[0].hint_value] if len(color_hints) else " "
                raw_hints_str += " "
            raw_hints_strs.append(raw_hints_str)
            #raw_hints_str = f"P{player}: [{' '.join([card.hints for card in cards])}]"
        output = "HINTS  : " + "  |  ".join(raw_hints_strs)
        output += "\nHANDS  : " + "  |  ".join(raw_cards_strs)
        output += "\nPLAYED : " + str(self.played) + f"        STRIKES: {self.strikes}        HINTS: {self.num_hints}"
        output += f"        CARDS LEFT: {len(self.deck)}\n"
        print(output)

    def shuffle_cards(self) -> List[Card]:
        deck = []
        for i in range(NUM_COLORS):
            deck.extend([
                Card(i, 1, []), Card(i, 1, []), Card(i, 1, []), Card(i, 2, []), Card(i, 2, []),
                Card(i, 3, []), Card(i, 3, []), Card(i, 4, []), Card(i, 4, []), Card(i, 5, [])
            ])
        random.shuffle(deck)
        return deck

    def deal_cards(self, deck: List[Card]) -> Tuple[Dict[int, List[Card]], List[Card]]:
        # 5 cards per player
        if self.num_players in {2, 3}:
            player_cards = {i: deck[i*5:(i+1)*5] for i in range(self.num_players)}
            deck = deck[self.num_players*5:]
            return player_cards, deck
        # 4 cards per player
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
            if last_played.number == 5:
                self.num_hints += 1
            return True
        return False

    def play_complete(self) -> int:
        done = False
        counting_down_out_of_cards = False
        count_down_out_of_cards = 0

        while not done:
            self.num_hints = min(self.num_hints, 8)
            for i, player in enumerate(self.players):
                visible_hands = {
                    j: player_cards for j, player_cards in self.player_cards.items() if i != j
                }
                new_action = player.play(
                    visible_hands
                )
                new_action.actor = i
                self.history.append(new_action)
                remaining_cards = True
                # Update state information for the new actions
                if isinstance(new_action, Play):
                    idx = new_action.idx
                    card = self.player_cards[i][idx]
                    new_action.card = card
                    new_action.success = True
                    if not self.play_card(card):
                        new_action.success = False
                        self.strikes += 1
                    remaining_cards = self.draw_new_card(i, idx)
                elif isinstance(new_action, Hint):
                    if self.num_hints <= 0:
                        raise IndentationError("you don't have any hints left, foo")
                    new_action.matches_cards = []
                    # Default to number, override with color if needed
                    matches = lambda card: new_action.hint_value == card.number
                    if new_action.hint_type == HintType.COLOR:
                        matches = lambda card: new_action.hint_value == card.color

                    has_match = False
                    for idx, card in enumerate(self.player_cards[new_action.player]):
                        if matches(card):
                            has_match = True
                            card.hints.append(new_action)
                            new_action.matches_cards.append(idx)
                    if not has_match:
                        raise ZeroDivisionError(f"dude stop cheating. you can't hint {new_action}, player {new_action.player} with {self.player_cards[new_action.player]} doesn't have any")

                    self.num_hints -= 1
                elif isinstance(new_action, Discard):
                    idx = new_action.idx
                    card = self.player_cards[i][idx]
                    new_action.card = card
                    self.num_hints += 1
                    remaining_cards = self.draw_new_card(i, idx)

                if self.verbose:
                    print('Player', i, 'does', new_action)

                for player in self.players:
                    player.event_tracker(new_action, num_hints=self.num_hints, strikes=self.strikes, played=self.played)

                if not remaining_cards and not counting_down_out_of_cards:
                    counting_down_out_of_cards = True
                    count_down_out_of_cards = self.num_players

                if self.strikes >= 3:
                    done = True
                    if self.verbose:
                        print('YOU LOST')
                    break

                if counting_down_out_of_cards:
                    count_down_out_of_cards -= 1
                    if not count_down_out_of_cards:
                        done = True
                        if self.verbose:
                            print('NO MOAR CARDS')
                        break

                if self.verbose:
                    self.print_game_state()

        return sum([card.number for card in self.played])

if __name__ == '__main__':
    random.seed(0)
    num_players = 4
    from smart_player import SmartPlayer
    from average_player import AveragePlayer
    game = HanabiGame(players=[SmartPlayer(i, 4, NUM_COLORS) for i in range(num_players)], verbose=True)

    print('Final Score:', game.play_complete())
    print(tabulate.tabulate(
        [game.history[i*num_players:(i+1)*num_players] for i in range(len(game.history) // num_players)],
        headers=[f'Player {x}' for x in range(num_players)]
    ))
