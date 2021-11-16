from dataclasses import dataclass
import enum

from typing import List, Optional
from action import Hint, INT_TO_COLOR_REPR

@dataclass
class Card:
    color: int
    number: int
    hints: List[Hint]

    def __repr__(self) -> str:
        return f"{self.number}{INT_TO_COLOR_REPR[self.color]}" + (" " + str(self.hints) if len(self.hints) else "")
