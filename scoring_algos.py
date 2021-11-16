import numpy as np
import random

from typing import List
from hanabi import HanabiGame
from dumb_player import SmartDumbPlayer
from smart_player import SmartPlayer

def print_stats(scores: List[int], strikes: int):
    print('mean', np.mean(scores), 'std', np.std(scores), 'min', np.min(scores), 'med', np.median(scores), 'max', np.max(scores), 'strike %', strikes / len(scores))

def score_algo(algo, tries=10000):
    scores = []
    count_wins = 0
    strikes = 0
    for i in range(tries):
        players = [algo(i, 4, 6) for i in range(4)]
        game = HanabiGame(players=players)
        score = game.play_complete()
        scores.append(score)
        strikes += (game.strikes >= 3)
        if score == 0:
            print("Hard Loss:", i, game.history)
        if score == 30:
            count_wins += 1
            print("WON!!!", count_wins)

    print_stats(scores, strikes)


if __name__ == '__main__':
    random.seed(0)
    score_algo(SmartPlayer, tries=10000)
