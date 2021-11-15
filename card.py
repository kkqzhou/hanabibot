from dataclasses import dataclass
import enum

from typing import List, Optional


class HintType(enum.Enum):
    COLOR = 0
    NUMBER = 1


@dataclass
class Hint:
    player: int
    hint_type: HintType
    hint_value: int # Matches hint_type, is color or number depending

    def __repr__(self) -> str:
        return f"H(p{self.player} {self.hint_type.name} {self.hint_value})"

@dataclass
class Card:
    color: int
    number: int
    hints: List[Hint]

    def __repr__(self) -> str:
        return f"C({self.color}/{self.number})" + (" " + str(self.hints) if len(self.hints) else "")
