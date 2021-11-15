import numpy as np

from typing import List
from hanabi import HanabiGame
from dumb_player import SmartDumbPlayer

def print_stats(scores: List[int]):
    print(np.mean(scores), np.median(scores), np.max(scores), np.min(scores), np.std(scores))

def score_algo(algo, tries=100000):
    scores = []
    for _ in range(tries):
        game = HanabiGame(players=[algo() for _ in range(4)])
        score = game.play_complete()
        scores.append(score)

    print_stats(scores)


if __name__ == '__main__':
    score_algo(SmartDumbPlayer)

