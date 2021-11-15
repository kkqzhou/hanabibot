from typing import Dict, List
from card import Card
from abc import ABC, abstractmethod

class Action:

    pass

class Player(ABC):
    @abstractmethod
    def play(self, who_am_i: int, other_hand: Dict[int, List[Card]], played: List[Card], history: List[Action]) -> Action:
        pass
