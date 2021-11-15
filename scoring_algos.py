import numpy as np
import random

from typing import List
from hanabi import HanabiGame
from dumb_player import SmartDumbPlayer
from retarded_player import RetardedPlayer

def print_stats(scores: List[int]):
    print('mean', np.mean(scores), 'std', np.std(scores), 'min', np.min(scores), 'med', np.median(scores), 'max', np.max(scores))

def score_algo(algo, tries=100000):
    scores = []
    for _ in range(tries):
        game = HanabiGame(players=[algo() for _ in range(4)])
        score = game.play_complete()
        scores.append(score)

    print_stats(scores)


if __name__ == '__main__':
    random.seed(0)
    score_algo(RetardedPlayer, tries=10000)

