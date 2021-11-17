from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union, List

INT_TO_COLOR_REPR = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', None: "."}

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
        hint_repr = INT_TO_COLOR_REPR[self.hint_value] if self.hint_type == HintType.COLOR else self.hint_value
        return f"H(p{self.player} {hint_repr})"

@dataclass
class Play:
    idx: int
    card: Optional[int] = None # Set by the controller, not by the player
    success: Optional[bool] = True
    actor: Optional[int] = None

    def __repr__(self) -> str:
        success_repr = '+' if self.success else '-'
        return f"P({repr(self.card)} {success_repr})"

@dataclass
class Discard:
    idx: int
    card: Optional[int] = None # Set by the controller, not the player
    actor: Optional[int] = None

    def __repr__(self) -> str:
        return f"X({repr(self.card)})"

Action = Union[Hint, Discard, Play]


