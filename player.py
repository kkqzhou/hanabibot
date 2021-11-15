from typing import Dict, List, Optional, Union
from card import Card
from abc import ABC, abstractmethod

import enum
from dataclasses import dataclass

class HintType(enum.Enum):
    COLOR = 0
    NUMBER = 1


@dataclass
class Play:
    idx: int
    card: Optional[int] = None # Set by the controller, not by the player
    success: bool = True


@dataclass
class Hint:
    player: int
    indices: List[int]
    hint_type: HintType

@dataclass
class Discard:
    idx: int
    card: Optional[int] = None # Set by the controller, not the player

Action = Union[Hint, Discard, Play]

class Player(ABC):
    @abstractmethod
    def play(self, who_am_i: int, other_hands: Dict[int, List[Card]], played: List[Card], discarded: List[Card], history: List[Action]) -> Action:
        pass
