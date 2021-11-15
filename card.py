from dataclasses import dataclass
import enum

from typing import List, Optional


class HintType(enum.Enum):
    COLOR = 0
    NUMBER = 1


@dataclass(frozen=True)
class Hint:
    player: int
    hint_type: HintType
    hint_value: int # Matches hint_type, is color or number depending

@dataclass
class Card:
    color: int
    number: int
    hints: List[Hint]
