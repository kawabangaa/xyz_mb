import numpy as np
from random import choice, choices, shuffle
from constants import b_value, r_value, d_value
from invoke_animal import invoke_animal, validate_board


class Game():

    def __init__(self, normal_turns_prob, animal_prob):
        self.normal_turns_prob = normal_turns_prob
        self.animal_prob = animal_prob
        self.reset()


    def reset(self):
        self.winner = None
        self.board = np.zeros((3, 3))
        self.moves_list = np.column_stack(np.where(self.board == 0))
        np.random.shuffle(self.moves_list)

    def set_probability(self, prob):
        self.prob = prob

    def check_game_finished(self):
        ret, self.winner = validate_board(self.board)
        return ret

    def play_round(self):
        # black turn
        # list_of_free_spots = np.column_stack(np.where(self.board == 0))
        if len(self.moves_list) == 1:
            selected = self.moves_list[0]
            self.board[selected[0]][selected[1]] = b_value
            self.moves_list = []
        elif len(self.moves_list) > 1:
            selected = self.moves_list[0]
            self.board[selected[0]][selected[1]] = b_value
            self.moves_list = self.moves_list[1:]
            if self.check_game_finished():
                return True
            selected = self.moves_list[0]
            self.board[selected[0]][selected[1]] = r_value
            self.moves_list = self.moves_list[1:]
            if self.check_game_finished():
                return True
        else:
            if self.check_game_finished():
                return True
        # pick animal
        if self.normal_turns_prob.draw_idx() > 0:
            self.board, self.moves_list = invoke_animal(self.board, self.moves_list, self.animal_prob)
            if self.check_game_finished():
                return True
        return False

    def play_game(self):
        finished = self.play_round()
        while not finished:
            finished = self.play_round()
        return self.winner
