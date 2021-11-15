from typing import Dict, List, Optional, Set, Union
from card import Card, Hint
from abc import ABC, abstractmethod

from dataclasses import dataclass


@dataclass
class Play:
    idx: int
    card: Optional[int] = None # Set by the controller, not by the player
    success: bool = True


@dataclass
class Discard:
    idx: int
    card: Optional[int] = None # Set by the controller, not the player

Action = Union[Hint, Discard, Play]

class Player(ABC):
    def __init__(self):
        pass

    def set_num_cards(self, num_cards):
        self.num_cards = num_cards
        #self.hints: List[Set[Hint]] = [set()] * num_cards

    #def receive_hint(self, idx_to_hint: Dict[int, Hint]):
    #    for idx, hint in idx_to_hint.items():
    #        self.hints[idx].add(hint)

    @abstractmethod
    def play(self,
        who_am_i: int,
        other_hands: Dict[int, List[Card]],
        played: List[Card],
        discarded: List[Card],
        history: List[Action],
        num_hints: int,
        strikes: int,
    ) -> Action:
        pass
