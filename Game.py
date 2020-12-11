import numpy as np
from random import choice, choices
from constants import b_value, r_value, d_value

class Game():

    def __init__(self):

        self.reset()
        pass

    def reset(self):
        self.winner = None
        self.board = np.zeros((3,3))

    def set_probability(self, prob):
        self.prob = prob

    def check_game_finished(self):
        B_WON = 3* b_value
        R_WON = 3* r_value
        values = np.append(
                            np.append(  self.board.sum(axis = 0),
                                        self.board.sum(axis = 1)),
                            [self.board[0][0] + self.board[1][1] + self.board[2][2],
                             self.board[0][2] + self.board[1][1] + self.board[2][0]])
        #     self.board.sum(axis = 0)
        # np.append(values, self.board.sum(axis = 1), axis = 0)
        # diag = [self.board[0][0] + self.board[1][1] + self.board[2][2],
        #         self.board[0][2] + self.board[1][1] + self.board[2][0]]
        # np.append(values,diag)
        for value in values:
            if value == B_WON:
                self.winner = b_value
                return True
            elif value == R_WON:
                self.winner = r_value
                return True
        if not(d_value in self.board):
            self.winner = d_value
            return True
        return False

    def play_round(self):
        # black turn
        list_of_free_spots = np.column_stack(np.where(self.board == 0))
        if len(list_of_free_spots) == 1:
            selected = list_of_free_spots[0]
            self.board[selected[0]][selected[1]] = b_value
        elif len(list_of_free_spots) > 1:
            selected = choices(list_of_free_spots, k=2)
            self.board[selected[0][0]][selected[0][1]] = b_value
            if self.check_game_finished():
                return True
            self.board[selected[1][0]][selected[1][1]] = r_value
            if self.check_game_finished():
                return True
        else:
            if self.check_game_finished():
                return True
        # pick animal

        return False

    def play_game(self):
        finished = self.play_round()
        while not finished:
            finished = self.play_round()
        return self.winner



