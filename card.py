from dataclasses import dataclass
import enum

from typing import List


class HintType(enum.Enum):
    COLOR = 0
    NUMBER = 1


@dataclass(frozen=True)
class Hint:
    player: int
    hint_type: HintType
    hint_value: int # Matches hint_type, is color or number depending

    def __repr__(self) -> str:
        return f"p{self.player} {self.hint_type.name} {self.hint_value}"


class Card:
    def __init__(self, color: int, number: int):
        self.color = color
        self.number = number
        self.hints: List[Hint] = []
    
    def add_hint(self, hint: Hint):
        self.hints.append(hint)

    def __repr__(self) -> str:
        return f"{self.color} {self.number} {self.hints}"
