from typing import Dict, List, Set
from card import Card
from abc import ABC, abstractmethod

from dataclasses import dataclass
from action import Action, Hint
from player import SimplePlayer

class OldPlayer(SimplePlayer):
    @abstractmethod
    def old_play(self,
        who_am_i: int,
        other_hands: Dict[int, List[Card]],
        played: List[Card],
        discarded: List[Card],
        history: List[Action],
        num_hints: int,
        strikes: int,
        my_card_hints: List[List[Hint]],
    ) -> Action:
        pass

    def play(self,
        other_hands: Dict[int, List[Card]]
    ) -> Action:
        return self.old_play(
            self.who_am_i,
            other_hands,
            self.played,
            self.discarded,
            self.history,
            self.num_hints,
            self.strikes,
            self.my_card_hints
        )
