import pandas as pd
from Game import Game
from Probability import Probability
from constants import *


def run_games(s_distribution, max_beast_weight, beast_weight_resolution, games_per_combination):
    """
    simulates different beast weights to find the ones with the smallest black-red win difference.
    """
    special_prob = Probability(2, s_distribution)
    draw_prob = Probability(2, [1, 0])
    idx = 0
    data = []
    for wasp_weight in range(1, max_beast_weight, beast_weight_resolution):
        for chameleon_weight in range(1, max_beast_weight, beast_weight_resolution):
            for snake_weight in range(1, max_beast_weight, beast_weight_resolution):
                for cheetah_weight in range(1, max_beast_weight, beast_weight_resolution):
                    # Generating the games
                    score = {BLACK_VALUE: 0, DRAW_VALUE: 0, RED_VALUE: 0}
                    if VERBOSE:
                        print("starting with new params: " + str(wasp_weight) + str(chameleon_weight) + str(
                            snake_weight) + str(cheetah_weight))
                    animal_prob = Probability(NUM_OF_BEASTS,
                                              [wasp_weight, chameleon_weight, snake_weight, cheetah_weight])
                    game = Game(special_prob, animal_prob, draw_prob)
                    for i in range(games_per_combination):
                        if VERBOSE:
                            print("starting game " + str(i))
                        score[game.play_game()] += 1
                        if VERBOSE:
                            print('result stake: ' + str(score))
                        game.reset()
                    # Converting results into percentages
                    factor = 100.0 / sum(score.values())
                    for k in score:
                        score[k] = score[k] * factor
                    if VERBOSE:
                        print("finished params, result: " + str(score))
                    # Inserting the data into the data list
                    data.append(
                        [wasp_weight, chameleon_weight, snake_weight, cheetah_weight, score[BLACK_VALUE],
                         score[RED_VALUE],
                         score[DRAW_VALUE]])
                    idx += 1
    df = pd.DataFrame(data, columns=[WASP_WEIGHT_COL_CONST, CHAM_WEIGHT_COL_CONST, SNAKE_WEIGHT_COL_CONST,
                                     CHEET_WEIGHT_COL_CONST, BLACK_PERC_COL_CONST, RED_PERC_COL_CONST,
                                     DRAW_PERC_COL_CONST])
    df[RED_BLACK_DIFF_COL_CONST] = (df[BLACK_PERC_COL_CONST] - df[RED_PERC_COL_CONST]).abs()
    return df


def run_and_plot_animal_prob(special_prob_dist, max_weight_per_animal, weight_resulotion, plays_per_comb):
    df = run_games(special_prob_dist, max_weight_per_animal, weight_resulotion, plays_per_comb)
    df.to_csv('animal_prob_exploration.csv')


if __name__ == '__main__':
    s_distribution = [2, 1]
    max_beast_weight = 5
    beast_weight_resolution = 1
    games_per_combination = 5000
    run_and_plot_animal_prob(s_distribution, max_beast_weight, beast_weight_resolution, games_per_combination)
