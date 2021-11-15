from player import Player, Action, Play
from typing import Dict, List
from card import Card

class DumbPlayer(Player):
    def play(self,
        who_am_i: int,
        other_hands: Dict[int, List[Card]],
        played: List[Card],
        discarded: List[Card],
        history: List[Action],
        hints: int,
        strikes: int,
    ) -> Action:
        return Play(0)
