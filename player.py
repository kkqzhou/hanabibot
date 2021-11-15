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

    @abstractmethod
    def play(self,
        who_am_i: int,
        other_hands: Dict[int, List[Card]],
        played: List[Card],
        discarded: List[Card],
        history: List[Action],
        num_hints: int,
        strikes: int,
        my_card_hints: List[List[Hint]],
    ) -> Action:
        pass
