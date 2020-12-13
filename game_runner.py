import csv
from Game import Game
from Probability import Probability
from constants import animal_cnt, num_of_animal, verbose
def run_games():
    res = {-1:0,0:0,1:0}
    special_prob = Probability(2,[2,1])
    loop_range = 3
    step_size = 1
    plays_per_comb = 100
    with open('result.csv', mode='w') as res_file:
        res_writer = csv.writer(res_file)
        for a in range(0,loop_range,step_size):
            for b in range(0,loop_range,step_size):
                for c in range(0,loop_range,step_size):
                    for d in range(0,loop_range,step_size):
                        if verbose:
                            print("starting with new params: "+ str(a) + str(b) + str(c) + str(d))
                        csv_row = []
                        csv_row.append(str(a))
                        csv_row.append(str(b))
                        csv_row.append(str(c))
                        csv_row.append(str(d))
                        animal_prob = Probability(num_of_animal,[a,b,c,d])
                        game = Game(special_prob, animal_prob)
                        for i in range(plays_per_comb):
                            if verbose:
                                print("starting game " + str(i))
                            res[game.play_game()] += 1
                            if verbose:
                                print('result stake: ' + str(res))
                            game.reset()
                        factor = 100.0 / sum(res.values())

                        for k in res:
                            csv_row.append(str(res[k] * factor))
                        if verbose:
                            print("finished params, result: "+ str(csv_row))
                        res_writer.writerow(csv_row)
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
    prob = Probability(3,[1,2,2])
    test = [0,0,0]
    for _ in range(1000):
        test[prob.draw_idx()] += 1
    print(test)

if __name__ == '__main__':
    #run_one_game()
    run_games()