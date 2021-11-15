class Player(ABC):
    def __init__(self, who_am_i: int):
        self.who_am_i = who_am_i
        self.history = []
        self.strikes = 0
        self.hints = 0

    @abstractmethod
    def play(self,
        other_hands: Dict[int, List[Card]],
    ) -> Action:
        pass

    @abstractmethod
    def event_tracker(self, event: Action):
        pass
