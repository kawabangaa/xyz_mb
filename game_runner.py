from Game import Game

def run_games(num):
    res = {-1:0,0:0,1:0}
    game = Game()
    for i in range(num):
        res[game.play_game()] += 1
        game.reset()
    factor = 100.0 / sum(res.values())
    for k in res:
        res[k] = res[k] * factor
    print(res)

if __name__ == '__main__':
    run_games(50000)