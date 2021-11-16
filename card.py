from dataclasses import dataclass
import enum

from typing import List, Optional
from action import Hint

@dataclass
class Card:
    color: int
    number: int
    hints: List[Hint]

    def __repr__(self) -> str:
        return f"C({self.color}/{self.number})" + (" " + str(self.hints) if len(self.hints) else "")
