import csv
import pandas as pd
from Game import Game
from Probability import Probability
from constants import animal_cnt, num_of_animal, verbose, b_value, r_value, d_value

def run_games(special_prob_dist, max_weight, weight_resulotion, plays_per_comb):

    special_prob = Probability(2,special_prob_dist)

    idx = 0
    data = []
    for wasp_weight in range(0, max_weight, weight_resulotion):
        for chameleon_weight in range(0, max_weight, weight_resulotion):
            for snake_weight in range(0, max_weight, weight_resulotion):
                for cheetah_weight in range(0, max_weight, weight_resulotion):
                    # Generating the games
                    res = {b_value: 0, d_value: 0, r_value: 0}
                    if verbose:
                        print("starting with new params: "+ str(wasp_weight) + str(chameleon_weight) + str(snake_weight) + str(cheetah_weight))
                    animal_prob = Probability(num_of_animal,[wasp_weight,chameleon_weight,snake_weight,cheetah_weight])
                    game = Game(special_prob, animal_prob)
                    for i in range(plays_per_comb):
                        if verbose:
                            print("starting game " + str(i))
                        res[game.play_game()] += 1
                        if verbose:
                            print('result stake: ' + str(res))
                        game.reset()
                    # Converting results into percentages
                    factor = 100.0 / sum(res.values())
                    for k in res:
                        res[k] = res[k] * factor
                    if verbose:
                        print("finished params, result: "+ str(res))
                    # Inserting the data into the data list
                    data.append([wasp_weight, chameleon_weight, snake_weight, cheetah_weight, res[b_value], res[r_value], res[d_value]])
                    idx += 1
    df = pd.DataFrame(data, columns=['wasp', 'chameleon', 'snake', 'cheetah', 'black_per', 'red_per', 'draw_per'])
    return df

def plot_games():
    df = run_games([2,1], 4, 1, 100)
    df.to_csv('result.csv')


def run_one_game():
    res = {-1: 0, 0: 0, 1: 0}
    plays_per_comb = 1000
    normal_prob = Probability(2, [2, 1])
    animal_prob = Probability(num_of_animal, [0, 1, 0, 0])
    game = Game(normal_prob, animal_prob)
    for i in range(plays_per_comb):
        res[game.play_game()] += 1
        game.reset()
    factor = 100.0 / sum(res.values())

    for k in res:
        res[k] = (res[k] * factor)
    print(res)

def test_probability():
    prob = Probability(3,[1,0,1])
    test = [0,0,0]
    for _ in range(1000):
        test[prob.draw_idx()] += 1
    print(test)

if __name__ == '__main__':
    #test_probability()
    #run_one_game()
    #run_games([2,1], 8, 1, 5000)
    plot_games()