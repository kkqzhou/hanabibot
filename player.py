from card import Card
from action import Action, Hint, Play, Discard
from abc import ABC, abstractmethod

from typing import List, Dict

class Player(ABC):
    def __init__(self, who_am_i: int, hand_size: int, num_colors: int):
        self.who_am_i = who_am_i
        self.hand_size = hand_size
        self.num_colors = num_colors

    @abstractmethod
    def play(self,
        other_hands: Dict[int, List[Card]],
    ) -> Action:
        pass

    def event_tracker(self, event: Action):
        pass

class SimplePlayer(Player):
    def __init__(self, who_am_i: int, hand_size: int, num_colors: int):
        super().__init__(who_am_i, hand_size, num_colors)
        self.history = []
        self.strikes = 0
        self.discarded = []
        self.num_hints = 8
        self.played = [Card(i, 0, []) for i in range(num_colors)]
        self.my_card_hints = [[] for _ in range(hand_size)]

    @abstractmethod
    def play(self,
        other_hands: Dict[int, List[Card]],
    ) -> Action:
        pass

    def update_self_hints(self, event: Action):
        if isinstance(event, Hint):
            self.num_hints -= 1
            if event.player == self.who_am_i:
                for idx in event.matches_cards:
                    self.my_card_hints[idx].append(event)

        # Manage my_card_hints for play and discard events
        if isinstance(event, (Play, Discard)):
            if event.actor == self.who_am_i:
                del self.my_card_hints[event.idx]
                self.my_card_hints.append([])

        if isinstance(event, Discard):
            self.num_hints += 1

    def update_discarded(self, event: Action):
        if isinstance(event, (Play, Discard)):
            self.discarded.append(event.card)

    def event_tracker(self, event: Action):
        self.history.append(event)
        self.update_self_hints(event)
        self.update_discarded(event)
        if isinstance(event, Play):
            if not event.success:
                self.strikes += 1
            else:
                self.played[event.card.color].number = event.card.number
