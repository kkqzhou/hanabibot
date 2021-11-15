from typing import Dict, List, Union
from card import Card
from abc import ABC, abstractmethod

class Play:
    def __init__(self, idx: int):
        self.idx = idx
        self.card = None # Set by the controller, not by the player
        self.success = True

class Hint:
    def __init__(self, player: int, indices: List[Card], hint_info: Card):
        self.player = player
        self.indices = indices
        self.hint_info = hint_info

class Discard:
    def __init__(self, idx: int):
        self.idx = idx
        self.card = None # Set by the controller, not the player

Action = Union[Hint, Discard, Play]

class Player(ABC):
    @abstractmethod
    def play(self, who_am_i: int, other_hands: Dict[int, List[Card]], played: List[Card], discarded: List[Card], history: List[Action]) -> Action:
        pass
