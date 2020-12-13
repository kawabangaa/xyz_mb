import numpy as np
from random import randint
from constants import b_value, r_value, verbose
from rounds import invoke_animal, validate_board


class Game():

    def __init__(self, normal_turns_prob, animal_prob, ):
        self.normal_turns_prob = normal_turns_prob
        self.animal_prob = animal_prob
        self.reset()


    def reset(self):
        self.winner = None
        self.board = np.zeros((3, 3))
        self.moves_list = np.column_stack(np.where(self.board == 0))
        np.random.shuffle(self.moves_list)

    def check_game_finished(self):
        ret, self.winner = validate_board(self.board)
        return ret

    def play_round(self):
        available_board_values = [b_value, r_value]
        if len(self.moves_list) == 1:
            value_idx = randint(0,1)
            selected = self.moves_list[0]
            self.board[selected[0]][selected[1]] = available_board_values[value_idx]
            self.moves_list = []
        elif len(self.moves_list) > 1:
            value_idx = randint(0, 1)
            for i in range(2):
                selected = self.moves_list[0]
                self.board[selected[0]][selected[1]] = available_board_values[value_idx]
                value_idx += 1
                value_idx %= 2
                self.moves_list = self.moves_list[1:]
                if self.check_game_finished():
                    return True
            # selected = self.moves_list[0]
            # self.board[selected[0]][selected[1]] = r_value
            # self.moves_list = self.moves_list[1:]
            # if self.check_game_finished():
            #     return True

            if self.normal_turns_prob.draw_idx() > 0:
                temp_board, temp_moves_list = invoke_animal(self.board, self.moves_list, self.animal_prob)
                self.board = temp_board
                self.moves_list = np.copy(temp_moves_list)
                if self.check_game_finished():
                    return True
        else:
            if self.check_game_finished():
                return True
        # pick animal

        return False

    def play_game(self):
        finished = self.play_round()
        if verbose:
            print(self.board)
            print(self.moves_list)
            print("finished a round")
        while not finished:
            finished = self.play_round()
            if verbose:
                print(self.board)
                print(self.moves_list)
                print("finished a round")
        return self.winner
