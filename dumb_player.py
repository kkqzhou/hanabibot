from action import Hint, HintType, Action, Play, Discard
from old_player import OldPlayer
from typing import Dict, List
from card import Card

class DumberPlayer(OldPlayer):
    def old_play(self,
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

class DumbPlayer(OldPlayer):
    def old_play(self,
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

class SmartDumbPlayer(OldPlayer):
    def old_play(self,
        who_am_i: int,
        other_hands: Dict[int, List[Card]],
        played: List[Card],
        discarded: List[Card],
        history: List[Action],
        hints: int,
        strikes: int,
        my_card_hints: List[List[Hint]],
    ) -> Action:
        # Iterated horrible code
        # Play
        # hint
        # discard
        # Plays all cards in order (i.e. all 1s all 2s all 3s...) can win but it is painful
        next_number = min(p.number for p in played) + 1
        playable_card_colors = set(p.color for p in played if p.number + 1 == next_number)
        hinted_colors = set()

        for i, my_hints in enumerate(my_card_hints):
            # Play known good cases always, i.e. I know the card + color is playable
            color = [hint for hint in my_hints if hint.hint_value in playable_card_colors and hint.hint_type == HintType.COLOR]
            if [hint for hint in my_hints if hint.hint_value == next_number and hint.hint_type == HintType.NUMBER] and color:
                return Play(i)

        for i, my_hints in reversed(list(enumerate(my_card_hints))):
            if [hint for hint in my_hints if hint.hint_value == next_number and hint.hint_type == HintType.NUMBER] and not \
                    [hint for hint in my_hints if hint.hint_value not in playable_card_colors and hint.hint_type == HintType.COLOR]:
                return Play(i)

        player_counts = dict()
        playable_card_count = 0
        for i, hand in other_hands.items():
            for card in hand:
                if card.number != next_number:
                    continue
                if card.color not in playable_card_colors:
                    continue
                if card.color in hinted_colors:
                    continue
                for hint in card.hints:
                    if hint.hint_type == HintType.NUMBER:
                        hinted_colors.add(card.color)

        for i, hand in other_hands.items():
            for card in hand:
                colors = set()
                if card.number == next_number:
                    if i not in player_counts:
                        player_counts[i] = 0
                    if card.color not in playable_card_colors and not any(hint for hint in card.hints if hint.hint_type == HintType.COLOR) and any(hint for hint in card.hints if hint.hint_type == HintType.NUMBER):
                        player_counts[i] -= 2
                        continue
                    if not any(hint for hint in card.hints if hint.hint_type == HintType.NUMBER) and card.color not in colors and card.color not in hinted_colors:
                        player_counts[i] += 1
                    if card.color in colors or card.color in hinted_colors or card.color not in playable_card_colors:
                        player_counts[i] -= 1

                    colors.add(card.color)

        max_value = 0
        next_player = None
        for i, count in player_counts.items():
            if count > max_value:
                next_player = i
                max_value = count
        bad_player = None
        min_value = 0
        for i, count in player_counts.items():
            if count < min_value:
                min_value = count
                bad_player = i

        if hints > 0:
            # Tell a player who would strike out not to strike out
            if bad_player is not None:
                bad_cards = list()
                for card in other_hands[bad_player]:
                    if any(hint for hint in card.hints if hint.hint_type == HintType.COLOR):
                        continue
                    if card.number != next_number:
                        continue
                    if card.color in playable_card_colors:
                        continue
                    bad_cards.append(card)
                if bad_cards:
                    bad_colors = dict()
                    for card in bad_cards:
                        if card.color not in bad_colors:
                            bad_colors[card.color] = 0
                        bad_colors[card.color] += 1
                    max_count = 0
                    bad_color = None
                    for color, count in bad_colors.items():
                        if max_count < count:
                            max_count = count
                            bad_color = color
                    return Hint(bad_player, HintType.COLOR, bad_color)

            if next_player is not None:
                return Hint(next_player, HintType.NUMBER, next_number)

        for i, my_hints in enumerate(my_card_hints):
            if [hint for hint in my_hints if hint.hint_value < next_number and hint.hint_type == HintType.NUMBER]:
                return Discard(i)

        return Discard(0)
