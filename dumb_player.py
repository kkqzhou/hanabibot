from player import Player, Action, Play
from typing import Dict, List
from card import Card, Hint, HintType

class DumberPlayer(Player):
    def play(self,
        who_am_i: int,
        other_hands: Dict[int, List[Card]],
        played: List[Card],
        discarded: List[Card],
        history: List[Action],
        hints: int,
        strikes: int,
        my_card_hints: List[List[Hint]],
    ) -> Action:
        return Hint((1 + who_am_i) % 4, HintType.NUMBER, 1)

class DumbPlayer(Player):
    def play(self,
        who_am_i: int,
        other_hands: Dict[int, List[Card]],
        played: List[Card],
        discarded: List[Card],
        history: List[Action],
        hints: int,
        strikes: int,
        my_card_hints: List[List[Hint]],
    ) -> Action:
        return Play(0)
