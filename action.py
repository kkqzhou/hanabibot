from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union, List

class HintType(Enum):
    COLOR = 0
    NUMBER = 1

@dataclass
class Hint:
    player: int
    hint_type: HintType
    hint_value: int # Matches hint_type, is color or number depending
    matches_cards: Optional[List[int]] = None # All the matching cards for the player
    actor: Optional[int] = None

    def __repr__(self) -> str:
        return f"H(p{self.player} {self.hint_type.name} {self.hint_value})"

@dataclass
class Play:
    idx: int
    card: Optional[int] = None # Set by the controller, not by the player
    success: Optional[bool] = True
    actor: Optional[int] = None

@dataclass
class Discard:
    idx: int
    card: Optional[int] = None # Set by the controller, not the player
    actor: Optional[int] = None

Action = Union[Hint, Discard, Play]


