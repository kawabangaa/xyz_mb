import pandas as pd
from Game import Game
from Probability import Probability
from constants import *




def run_games(special_prob_dist, selected_animal_prob, golden_draw_percentage, draw_max_weight, draw_resulotion, plays_per_comb):
    """
    given s, b probabilities and g (golden draw percentage) tries different draw tactic probabilities (d)
    to search for the best d. the search is a for loop over different possibilities.
    """
    special_prob = Probability(2, special_prob_dist)
    animal_prob = Probability(NUM_OF_BEASTS, selected_animal_prob)
    idx = 0
    data = []
    for draw_weight in range(1, draw_max_weight, draw_resulotion):
        # Generating the games
        res = {BLACK_VALUE: 0, DRAW_VALUE: 0, RED_VALUE: 0}
        draw_prob = Probability(2, [draw_max_weight - draw_weight, draw_weight])
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
        data.append([draw_weight, draw_max_weight, res[BLACK_VALUE], res[RED_VALUE], res[DRAW_VALUE],
                     special_prob_dist[1] / sum(special_prob_dist)])
        idx += 1
    df = pd.DataFrame(data,
                      columns=[DRAW_WEIGHT_COL, DRAW_MAX_WEIGHT_COL, BLACK_PERC_COL_CONST, RED_PERC_COL_CONST, DRAW_PERC_COL_CONST])
    df[DRAW_DIFF_FROM_GOLDEN_COL] = (df[DRAW_PERC_COL_CONST] - golden_draw_percentage).abs()
    return df


def run_and_plot_draw_prob(s, b, g):
    df = run_games(s, b, g, 100, 10, 1000)
    df.to_csv('draw_prob.csv')


if __name__ == '__main__':
    g = 25 # in percentages
    s = [2, 1] # weights
    b = [0.273, 0.364, 0.273, 0.09] # selected beast probability
    run_and_plot_draw_prob(s, b, g)
