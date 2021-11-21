from action import Action, Play, Discard, Hint, HintType
from player import Player
from typing import Dict, List, Callable, Optional, Tuple
from card import Card

from copy import deepcopy

class SmartPlayer(Player):
    """
    This guy is supposed to be smart. Obviously he isn't
    """
    def __init__(self, who_am_i: int, hand_size: int, num_colors: int):
        super().__init__(who_am_i, hand_size, num_colors)
        self.x = 0
        self.num_hints: int = 8
        self.strikes: int = 0
        self.played = [Card(color, 0, []) for color in range(num_colors)]
        self.my_hints = [None] * hand_size

        number_counts = {1: 3, 2: 2, 3: 2, 4: 2, 5: 1}
        self.cards_still_alive = {(color, number): c for color in range(num_colors) for number, c in number_counts.items()}

    def print_my_info(self):
        print(f'Strikes: {self.strikes}    Hints: {self.num_hints}    Played {self.played}    My hints: {self.my_hints}')

    def right_player(self, n: int) -> int:
        return (self.who_am_i + n) % (len(self.other_hands) + 1)

    def event_tracker(self, event: Action, num_hints: int, strikes: int, played: List[Card], **kwargs):
        self.num_hints = num_hints
        self.strikes = strikes
        self.played = played

        if isinstance(event, Hint) and self.who_am_i == event.player:
            for idx in event.matches_cards:
                self.my_hints[idx] = event

        elif isinstance(event, Discard):
            self.cards_still_alive[(event.card.color, event.card.number)] -= 1

        elif isinstance(event, Play):
            self.cards_still_alive[(event.card.color, event.card.number)] -= 1


    @property
    def all_playables(self) -> List[Card]:
        return [x + 1 for x in self.played]
    
    def play(self, other_hands: Dict[int, List[Card]]) -> Action:
        #if not len(self.other_hands):
        self.other_hands = other_hands
        self.x += 1
        
        self.print_my_info()
        right_player = self.right_player(1)
        return Play(0) if self.x % 2 == 0 else Hint(right_player, HintType.NUMBER, self.other_hands[right_player][0].number)
        #