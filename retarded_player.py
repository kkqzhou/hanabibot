from action import Action, Play, Discard, Hint, HintType
from old_player import OldPlayer
from typing import Dict, List, Optional
from card import Card


def eq(card1: Card, card2: Card):
    return (card1.number == card2.number) and (card1.color == card2.color)


def get(hand: List[Card], hint_type: HintType, hint_value: int, _type: str):
    if hint_type == HintType.NUMBER:
        matching_cards = [x for x in hand if x.number == hint_value]
    if hint_type == HintType.COLOR:
        matching_cards = [x for x in hand if x.color == hint_value]
    return matching_cards[0] if _type == 'leftmost' else matching_cards[-1]


def hint_exists_on_card(card: Card, impending_hint: Hint):
    _impending_hint = (impending_hint.hint_type, impending_hint.hint_value)
    return _impending_hint in {(hint.hint_type, hint.hint_value) for hint in card.hints}


def is_problem_card(card: Card, discarded: List[Card]):
    if card.number in {2}:
        return True
    if card.number in {3} and (card.color, card.number) in {(card.color, card.number) for card in discarded}:
        return True
    return False


def get_leftmost_unhinted(hand: List[Card]) -> Optional[Card]:
    unhinted = [card for card in hand if not len(card.hints)]
    return unhinted[0] if len(unhinted) else None


class RetardedPlayer(OldPlayer):
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
        
        my_leftmost_unhinted_idx = 0
        for idx, _hints in enumerate(my_card_hints):
            if not len(_hints):
                my_leftmost_unhinted_idx = idx
                break

        if hints == 0:
            return Discard(my_leftmost_unhinted_idx)

        # BE A NICE PERSON AND WARN PEOPLE ABOUT PROBLEM CARDS BEFORE PLAYING YOUR OWN
        for player, hand in other_hands.items():
            player_leftmost_unhinted = get_leftmost_unhinted(hand)
            if player_leftmost_unhinted is not None and is_problem_card(player_leftmost_unhinted, discarded):
                hint = Hint(player, HintType.NUMBER, player_leftmost_unhinted.number)
                if not hint_exists_on_card(player_leftmost_unhinted, hint):
                    return hint
        
        colors_with_no_1s_played = [i for i, card in enumerate(played) if card.number == 0]
        colors_with_1s_played = [i for i, card in enumerate(played) if card.number >= 1]

        # play my cards
        for i in range(len(my_card_hints)):
            idx = len(my_card_hints) - i - 1
            _hints = my_card_hints[idx]
            if sum([(hint.hint_value == 1) and (hint.hint_type == HintType.NUMBER) for hint in _hints]) > 0:
                return Play(idx) if len(colors_with_no_1s_played) else Discard(idx)
            if sum([(hint.hint_type == HintType.COLOR) for hint in _hints]) > 0:
                return Play(idx)

        # hint others
        for player, hand in other_hands.items():
            if sum([(card.number == 1) and (card.color in colors_with_no_1s_played) for card in hand]) > 0:
                hint = Hint(player, HintType.NUMBER, 1)
                if sum([hint_exists_on_card(card, hint) for card in hand]) == 0:
                    return hint

            for color in colors_with_1s_played:
                num_on_top = played[color].number
                next_card_on_top = Card(color, num_on_top + 1, [])
                if sum([eq(next_card_on_top, card) for card in hand]) == 0:
                    continue

                rightmost_color_card = get(hand, HintType.COLOR, color, 'rightmost')
                impending_hint = Hint(player, HintType.COLOR, color)
                if eq(rightmost_color_card, next_card_on_top) and not hint_exists_on_card(rightmost_color_card, impending_hint):
                    return impending_hint

        return Discard(my_leftmost_unhinted_idx)
