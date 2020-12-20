import pandas as pd
from Game import Game
from Probability import Probability
from constants import *


def run_games(special_prob_dist, top_configurations, plays_per_comb):
    """
    runs a in depth simulation of the top beast probabilities
    """
    special_prob = Probability(2, special_prob_dist)
    draw_prob = Probability(2, [1, 0])  # in this mode we are not exploring the draw probabilities
    idx = 0
    data = []
    for animal_prob_dist in top_configurations:
        # Generating the games
        res = {BLACK_VALUE: 0, DRAW_VALUE: 0, RED_VALUE: 0}
        animal_prob = Probability(NUM_OF_BEASTS, animal_prob_dist)
        game = Game(special_prob, animal_prob, draw_prob)
        for i in range(plays_per_comb):
            if VERBOSE:
                print("starting game " + str(i))
            res[game.play_game()] += 1
            if VERBOSE:
                print('result stake: ' + str(res))
            game.reset()
        # Converting results into percentages
        factor = 100.0 / sum(res.values())
        for k in res:
            res[k] = res[k] * factor
        if VERBOSE:
            print("finished params, result: " + str(res))
        # Inserting the data into the data list
        data.append(
            [animal_prob_dist[0], animal_prob_dist[1], animal_prob_dist[2], animal_prob_dist[3], res[BLACK_VALUE],
             res[RED_VALUE], res[DRAW_VALUE], ])
        idx += 1
    df = pd.DataFrame(data, columns=[WASP_WEIGHT_COL_CONST, CHAM_WEIGHT_COL_CONST, SNAKE_WEIGHT_COL_CONST,
                                     CHEET_WEIGHT_COL_CONST, BLACK_PERC_COL_CONST, RED_PERC_COL_CONST,
                                     DRAW_PERC_COL_CONST])
    df[RED_BLACK_DIFF_COL_CONST] = (df[BLACK_PERC_COL_CONST] - df[RED_PERC_COL_CONST]).abs()
    return df


def run_and_plot_top_animal_prob(top_configurations):
    df = run_games([2, 1], top_configurations, 100000)
    df.to_csv('top_animal_prob_ranked.csv')


if __name__ == '__main__':
    top_beast_probabilities =   [[1,2,3,2],
                                    [3,1,2,1],
                                    [3,4,4,2],
                                    [3,1,2,4],
                                    [4,3,3,3]]

    run_and_plot_top_animal_prob(top_beast_probabilities)
