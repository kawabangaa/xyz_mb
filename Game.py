import numpy as np
from random import randint
from constants import b_value, r_value,d_value, verbose
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

    def play_turn(self, color, tactic = "random"):
        if tactic == "random":
            selected = self.moves_list[0]
            self.board[selected[0]][selected[1]] = color
            if len(self.moves_list) > 0:
                self.moves_list = self.moves_list[1:]
            else:
                self.moves_list = []
        elif tactic == "draw":
            opposite_color = color * -1
            #checking if in one of the columns there're 2 of the opposite color and a 0
            cols_sum = self.board.sum(axis=0)
            col_indices = self.board[:,np.where(cols_sum == opposite_color * 2)]
            if col_indices.size > 0:
                col_indices = np.where(col_indices.reshape((1,3))==d_value)
                self.board[col_indices] = color
                self.moves_list.remove([col_indices[0][0],col_indices[1][0]])
                return
            # checking if in one of the rows there're 2 of the opposite color and a 0
            rows_sum = self.board.sum(axis=1)
            row_indices = self.board[np.where(rows_sum == opposite_color * 2), :]
            if row_indices.size > 0:
                row_indices = np.where(row_indices.reshape((1, 3)) == d_value)
                self.board[row_indices] = color
                self.moves_list.remove([row_indices[0][0], row_indices[1][0]])
                return
            # checking if in one of the diagonals there're 2 of the opposite color and a 0
            both_diag_indices = [[[0,0],[1,1],[2,2]],[[0,2],[1,1],[2,0]]]
            for diag_indices in both_diag_indices:
                diag_sum = 0
                for indices in diag_indices:
                    diag_sum += self.board[indices[0],indices[1]]
                if diag_sum == opposite_color * 2:
                    for indices in diag_indices:
                        if self.board[indices[0],indices[1]] == d_value:
                            self.board[indices[0], indices[1]] = color
                            self.moves_list.remove([indices[0], indices[1]])
                            return


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
