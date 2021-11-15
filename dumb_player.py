from player import Player, Action, Play, Discard
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

class SmartDumbPlayer(Player):
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
        next_number = min(p.number for p in played) + 1

        for i, my_hints in enumerate(my_card_hints):
            if [hint for hint in my_hints if hint.hint_value == next_number]:
                return Play(i)
        next_player = None
        for i, hand in other_hands.items():
            for card in hand:
                if card.number == next_number and not card.hints:
                    next_player = i

        if hints > 0 and next_player is not None:
            return Hint(next_player, HintType.NUMBER, next_number)

        return Discard(0)
