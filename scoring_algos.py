import numpy as np
import random

from typing import List
from hanabi import HanabiGame
from dumb_player import SmartDumbPlayer
from average_player import AveragePlayer
from smart_player import SmartPlayer

def print_stats(scores: List[int], strikes: int, wins: int):
    strike_perc = strikes / len(scores) * 100 # Displayed as perc
    win_perc = wins / len(scores) * 100 # Displayed as perc
    print('mean', np.mean(scores), 'std', np.std(scores), 'min', np.min(scores), 'med', np.median(scores), 'max', np.max(scores), 'strike %', strike_perc, 'win %', win_perc)

def score_algo(algo, tries=10000):
    scores = []
    count_wins = 0
    strikes = 0
    for i in range(tries):
        if i % 1000 == 999:
            print(f'Run {i+1}/{tries}')
        players = [algo(i, 4, 6) for i in range(4)]
        verbose = False
        if verbose:
            # Hack for smart player
            for p in players:
                p.verbose = True
        game = HanabiGame(players=players, verbose = verbose)
        score = game.play_complete()
        scores.append(score)
        strikes += (game.strikes >= 3)
        if score == 0:
            print("Hard Loss:", i, game.history)
        if score == 30:
            count_wins += 1
            print("WON!!!", count_wins)

    print_stats(scores, strikes, count_wins)


if __name__ == '__main__':
    random.seed(0)
    score_algo(AveragePlayer, tries=10000)
