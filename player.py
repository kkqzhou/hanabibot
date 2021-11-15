from typing import Dict, List
from card import Card
from abc import ABC, abstractmethod

class Action:
    pass

class Player(ABC):
    @abstractmethod
    def play(self, whoAmI: int, otherHands: Dict[int, List[Card]], played: List[Card], history: List[Action]) -> Action:
        pass
