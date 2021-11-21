from action import Action, Play, Discard, Hint, HintType
from player import Player
from typing import Dict, List, Callable, Optional, Tuple
from card import Card
import copy

from collections import defaultdict

class AveragePlayer(Player):
    """
    This is still pretty local shit, no finense or ordering for playablity 
    """
    def __init__(self, who_am_i: int, hand_size: int, num_colors: int):
        super().__init__(who_am_i, hand_size, num_colors)
        self.strikes = 0
        self.num_hints = 8
        self.verbose = False

        build_hints = lambda: [[Card(None, None, []), False] for _ in range(hand_size)]
        self.player_hints = defaultdict(build_hints)
        self.played = [Card(i, 0, []) for i in range(num_colors)]
        build_counts = lambda: {
            1: 3,
            2: 2,
            3: 2,
            4: 2,
            5: 1,
        }
        self.cards_remaining = defaultdict(build_counts)

    @classmethod
    def is_dead_card(cls,
        hints: Card,
        played: List[Card],
    ) -> bool:
        """
        Not looking at other peoples hands, check if a card is definitely dead

        Also doesn't look at discards
        """
        min_number = 0
        max_number = 5
        if hints.color is not None:
            min_number = played[hints.color].number + 1

        if hints.number is not None:
            max_number = hints.number

        return max_number < min_number

    @classmethod
    def is_playable_dumb(cls,
        hints: Card,
        played: List[Card],
    ) -> bool:
        """
        Not looking at other peoples hands, check if a card is potentially playable
        """
        color = hints.color
        number = hints.number
        if color is None and number is None:
            return False

        can_play_pure_number = True
        can_play_pure_color = True
        can_play_number_color = True
        if number is not None:
            # Check if this number is ever playable
            can_play_pure_number = False
            for p in played:
                if p.number == number - 1:
                    can_play_pure_number = True
                    break

        if color is not None:
            # Can play anything of this color
            can_play_pure_color = played[color].number < 5

        if color is not None and number is not None:
            can_play_number_color = played[color].number == number - 1

        return can_play_pure_color and can_play_pure_number and can_play_number_color

    @classmethod
    def discard_rule(cls,
        my_hints: List[Tuple[Card, bool]],
        played: List[Card],
    ) -> Action:
        # Discard leftmost card without info
        for i, known_info in enumerate(my_hints):
            known_info = known_info[0]
            card_color = known_info.color
            card_number = known_info.number
            # No info
            if card_color is None and card_number is None:
                return Discard(i)
            if cls.is_dead_card(known_info, played):
                return Discard(i)

        return Discard(0)

    @classmethod
    def play_rule(cls,
        my_hints: List[Tuple[Card, bool]],
        played: List[Card],
        playable_rule: Callable[[Card, List[Card]], bool],
    ) -> Optional[Action]:
        # Play rightmost, if it seems playable
        #   Assumed hinted + potentially playable = playable
        for i, known_info in reversed(list(enumerate(my_hints))):
            hints = known_info[0]
            # Do not play known blocking hints
            if (hints.color is None or hints.number is None) and known_info[1]:
                continue
            if playable_rule(hints, played):
                return Play(i)

        # Default to playing nothing
        return None

    @classmethod
    def play_or_discard_dumb(cls,
        my_hints: List[Tuple[Card, bool]],
        played: List[Card],
    ) -> Action:
        play_action = cls.play_rule(my_hints, played, cls.is_playable_dumb)
        if play_action:
            return play_action
        return cls.discard_rule(my_hints, played)

    def first_problem(self, other_hands: List[List[Card]]) -> Optional[Action]:
        # Solve problems one by one, solve next players problems with priority
        number_of_players = len(other_hands) + 1
        players_in_order = [(self.who_am_i + i + 1) % number_of_players for i in range(number_of_players - 1)]
        for player in players_in_order:
            actual_hand = other_hands[player]
            hints = self.player_hints[player]
            action = self.play_or_discard_dumb(hints, self.played)
            action.actor = player
            if action.idx >= len(actual_hand):
                continue
            action.card = actual_hand[action.idx]
            if isinstance(action, Play):
                card_played = actual_hand[action.idx]
                if not self.is_playable_dumb(card_played, self.played):
                    return action
            if isinstance(action, Discard):
                card_discard = actual_hand[action.idx]
                if self.is_dead_card(card_discard, self.played):
                    continue
                # Not dead, check if there is another copy of it
                if self.cards_remaining[card_discard.color][card_discard.number] == 1:
                    return action
        return None

    def fix_first_problem(self, other_hands: List[List[Card]]) -> Optional[Action]:
        first_problem = self.first_problem(other_hands)
        if not first_problem:
            return None

        # A bad card is played or discarded, just always hint it, unless that would mark it as playable
        # Only mark it as playable if it is playable
        bad_player = first_problem.actor
        bad_card_idx = first_problem.idx
        actual_card = first_problem.card
        other_hand = other_hands[bad_player]
        current_info = self.player_hints[bad_player][bad_card_idx][0]
        missing_color = current_info.color is None
        missing_number = current_info.number is None
        if missing_color:
            color_hint = Hint(bad_player, HintType.COLOR, actual_card.color)
            pure_info = Card(actual_card.color, None, [])
            if not self.is_playable_dumb(pure_info, self.played):
                return color_hint
            new_info = Card(actual_card.color, current_info.number, [])
            matches_color = lambda card: card.color == actual_card.color
            all_good = True
            for i, card in reversed(list(enumerate(other_hand))):
                if matches_color(card):
                    if self.is_playable_dumb(card, self.played):
                        break
                    card_info = self.player_hints[bad_player][i][0]
                    new_info = Card(actual_card.color, card_info.number, [])
                    if self.is_playable_dumb(new_info, self.played) and not self.is_playable_dumb(card, self.played):
                        all_good = False

            if all_good:
                return color_hint

        if missing_number:
            number_hint = Hint(bad_player, HintType.NUMBER, actual_card.number)
            pure_info = Card(None, actual_card.number, [])
            if not self.is_playable_dumb(pure_info, self.played):
                return number_hint
            new_info = Card(current_info.color, actual_card.number, [])
            matches_number = lambda card: card.number == actual_card.number
            all_good = True
            for i, card in reversed(list(enumerate(other_hand))):
                if matches_number(card):
                    if self.is_playable_dumb(card, self.played):
                        break
                    card_info = self.player_hints[bad_player][i][0]
                    new_info = Card(card_info.color, actual_card.number, [])
                    if self.is_playable_dumb(new_info, self.played) and not self.is_playable_dumb(card, self.played):
                        all_good = False
            if all_good:
                return number_hint
        return None

    def give_play_hint(self, other_hands):
        best_hint = None
        best_hint_count = 0
        best_negative_hint_count = 0
        playable_number_colors = set()
        for player, hand in other_hands.items():
            for idx, (hint, _) in enumerate(self.player_hints[player]):
                if idx < len(hand):
                    actual_card = hand[idx]
                else:
                    continue
                if self.is_playable_dumb(hint, self.played):
                    playable_number_colors.add((actual_card.color, actual_card.number))

        for player, hand in other_hands.items():
            hint_options = []
            for card in hand:
                # All playable cards, must find at least one for it to be worth a hint
                if self.is_playable_dumb(card, self.played):
                    new_card = Card(None, card.number, [])
                    hint_options.append(new_card)
                    new_card = Card(card.color, None, [])
                    hint_options.append(new_card)
            for option_real in hint_options:
                # None will never match, so just check color or number to check for a match
                option_func = lambda card: (card.number == option_real.number) or (card.color == option_real.color)
                played = [Card(p.color, p.number, []) for p in self.played]
                played_count = 0
                negative_hint_count = 0
                for idx, card in reversed(list(enumerate(hand))):
                    if self.verbose:
                        print(option_func(card), played_count, negative_hint_count, idx, card, option_real)
                    if option_func(card):
                        players_info = self.player_hints[player][idx][0]
                        can_play = not self.player_hints[player][idx][1]
                        # Disregard if the person is already playing it or someone else is playing it
                        if (can_play and self.is_playable_dumb(players_info, played)):
                            continue
                        if self.verbose:
                            print(card.color, card.number, playable_number_colors)
                        if self.is_playable_dumb(card, played) and not (card.color, card.number) in playable_number_colors:
                            played_count += 1
                            played[card.color].number += 1
                        else:
                            all_hints = Card(option_real.color or players_info.color, option_real.number or players_info.number, [])
                            if self.is_playable_dumb(all_hints, played):
                                # Count mistakes here as bad
                                negative_hint_count += 1
                                if played_count == 0:
                                    # First unplayable, giveup
                                    break
                if played_count > best_hint_count or (played_count == best_hint_count and best_negative_hint_count > negative_hint_count):
                    best_hint_count = played_count
                    best_hint = (player, option_real)
                    best_negative_hint_count = negative_hint_count
                    if self.verbose:
                        print(best_hint_count, best_hint, best_negative_hint_count)

        if best_hint:
            player, hint_deets = best_hint
            if hint_deets.color is not None:
                return Hint(player, HintType.COLOR, hint_deets.color)
            if hint_deets.number is not None:
                return Hint(player, HintType.NUMBER, hint_deets.number)

        return None


    def play(self,
        other_hands: Dict[int, List[Card]]
    ) -> Action:
        # Problem hints here should be solved
        fix_problem = self.fix_first_problem(other_hands)
        if fix_problem and self.num_hints > 0:
            return fix_problem

        # Play with priority
        my_hints = self.player_hints[self.who_am_i]
        play_action = self.play_rule(my_hints, self.played, self.is_playable_dumb)
        if play_action:
            return play_action

        # Give playable hints
        good_hint = self.give_play_hint(other_hands)
        if good_hint and self.num_hints > 0:
            return good_hint

        return self.discard_rule(my_hints, self.played)

    def event_tracker(self, event: Action, **kwargs):
        if isinstance(event, Hint):
            self.num_hints -= 1
            any_playable = False
            for idx in event.matches_cards:
                card = self.player_hints[event.player][idx][0]
                self.player_hints[event.player][idx][1] = False # Reset hints
                if event.hint_type == HintType.COLOR:
                    card.color = event.hint_value
                if event.hint_type == HintType.NUMBER:
                    card.number = event.hint_value
                if self.is_playable_dumb(card, self.played):
                    any_playable = True
            if not any_playable:
                for idx in event.matches_cards:
                    self.player_hints[event.player][idx][1] = True

        # A card is removed, modify hints accordingly
        if isinstance(event, (Play, Discard)):
            hints = self.player_hints[event.actor]
            del hints[event.idx]
            hints.append([Card(None, None, []), False])
            self.cards_remaining[event.card.color][event.card.number] -= 1

        if isinstance(event, Discard):
            self.num_hints += 1

        if isinstance(event, Play):
            if not event.success:
                self.strikes += 1
            else:
                self.played[event.card.color].number = event.card.number
