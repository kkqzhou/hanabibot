from dataclasses import dataclass
import enum

from typing import List, Optional
from action import Hint, INT_TO_COLOR_REPR, HintType

@dataclass
class Card:
    color: int
    number: int
    hints: List[Hint]

    def __eq__(self, other) -> bool:
        return (self.color == other.color) and (self.number == other.number)

    def __add__(self, other: int) -> "Card":
        return Card(self.color, self.number + other, self.hints)

    def __str__(self) -> str:
        return f"{self.number}{INT_TO_COLOR_REPR[self.color]}"

    def __repr__(self) -> str:
        return f"{self.number}{INT_TO_COLOR_REPR[self.color]}" + (" " + str(self.hints) if len(self.hints) else "")


assert Card(2, 3, []) == Card(2, 3, [])
assert Card(0, 4, [Hint(1, HintType.COLOR, 0)]) == Card(0, 4, [Hint(2, HintType.COLOR, 0), Hint(3, HintType.NUMBER, 4)])
assert Card(0, 4, [Hint(1, HintType.COLOR, 0)]) != Card(0, 5, [Hint(1, HintType.COLOR, 0)])
assert Card(2, 3, []) + 2 == Card(2, 5, [])
