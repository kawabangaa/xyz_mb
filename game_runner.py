from Game import Game
from Probability import Probability
from constants import animal_cnt, num_of_animal
def run_games(num):
    res = {-1:0,0:0,1:0}
    normal_prob = Probability(2,[7,3])
    animal_prob = Probability(num_of_animal,[0,0,0,1])
    game = Game(normal_prob, animal_prob)
    for i in range(num):
        res[game.play_game()] += 1
        game.reset()
    factor = 100.0 / sum(res.values())
    for k in res:
        res[k] = res[k] * factor
    print(res)
    print(animal_cnt)

def test_probability():
    prob = Probability(3,[1,2,2])
    test = [0,0,0]
    for _ in range(1000):
        test[prob.draw_idx()] += 1
    print(test)

if __name__ == '__main__':
    run_games(10000)