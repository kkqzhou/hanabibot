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

        self.my_hints = [None] * hand_size
        self.played = [Card(i, 0, []) for i in range(num_colors)]

        number_counts = {1: 3, 2: 2, 3: 2, 4: 2, 5: 1}
        self.cards_still_alive = {(color, number): c for color in range(num_colors) for number, c in number_counts.items()}

    def right_player(self, n):
        return (self.who_am_i + n) % (len(self.other_hands) + 1)

    def event_tracker(self, event: Action):
        return super().event_tracker(event)
    
    def play(self, other_hands: Dict[int, List[Card]]) -> Action:
        #if not len(self.other_hands):
        self.other_hands = other_hands
        self.x += 1
        
        print(self.other_hands)
        return Play(0) if self.x % 2 == 0 else Hint(self.right_player(1), HintType.NUMBER, 1)
        #