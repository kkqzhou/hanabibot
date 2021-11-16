from player import Player, Action, Play, Discard
from typing import Dict, List
from card import Card, Hint, HintType

class SmartPlayer(Player):
    def __init__(self):
        pass

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


