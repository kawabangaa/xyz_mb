from Game import Game
from Probability import Probability

def play_xyz(s, d, b):
    game = Game(s, b, d)
    game.play_game()


if __name__ == '__main__':
    s = Probability(2,[2, 1])
    d = Probability(2,[59, 41])
    b = Probability(4,[4,3,3,3])
    play_xyz(s, d, b)
