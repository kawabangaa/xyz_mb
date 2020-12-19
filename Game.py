import numpy as np
from random import randint
from constants import b_value, r_value,d_value, verbose
from rounds import invoke_animal, validate_board


class Game():

    def __init__(self, special_prob, animal_prob, draw_prob):
        self.special_prob = special_prob
        self.animal_prob = animal_prob
        self.draw_prob = draw_prob
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
            if verbose:
                self.print_status("start of tactic")
            opposite_color = color * -1
            #checking if in one of the columns there're 2 of the opposite color and a 0
            cols_sum = self.board.sum(axis=0)
            col_idx = np.where(cols_sum == opposite_color * 2)
            row = self.board[:, col_idx]
            if row.size > 0:
                row_idx = np.where(row.reshape((3,)) == d_value)
                self.board[row_idx, col_idx] = color
                if verbose:
                    self.print_status("end of col")
                    print("col_indices: " + str([row_idx[0][0], col_idx[0][0]]))
                    print("np all "+ str(np.all(self.moves_list == [row_idx[0], col_idx[0]])))
                self.moves_list = np.delete(self.moves_list, np.where(np.all(self.moves_list == [row_idx[0][0], col_idx[0][0]], axis=1)), axis=0)
                return
            # checking if in one of the rows there're 2 of the opposite color and a 0
            rows_sum = self.board.sum(axis=1)
            row_idx =np.where(rows_sum == opposite_color * 2)
            col = self.board[row_idx, :]
            if col.size > 0:
                col_idx = np.where(col.reshape((3,)) == d_value)
                self.board[row_idx, col_idx] = color
                if verbose:
                    self.print_status("end of row")
                    print("row_indices: " + str([row_idx[0][0], col_idx[0][0]]))
                    print("np all " + str(np.all(self.moves_list == [row_idx[0], col_idx[0]])))
                self.moves_list = np.delete(self.moves_list, np.where(np.all(self.moves_list == [row_idx[0][0], col_idx[0][0]], axis=1)), axis=0)
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
                            if verbose:
                                self.print_status("end of diag")
                                print("diag_indices: " + str([indices[0], indices[1]]))
                            self.moves_list = np.delete(self.moves_list,
                                                        np.where(np.all(self.moves_list == [indices[0], indices[1]], axis=1)),
                                                        axis=0)
                            return
            # else, just play random
            selected = self.moves_list[0]
            self.board[selected[0]][selected[1]] = color
            if len(self.moves_list) > 0:
                self.moves_list = self.moves_list[1:]
            else:
                self.moves_list = []


    def play_round(self):
        available_board_values = [b_value, r_value]
        if len(self.moves_list) == 1:
            value_idx = randint(0,1)
            self.play_turn(available_board_values[value_idx], self.tactics[available_board_values[value_idx]])
            if self.check_game_finished():
                return True

        elif len(self.moves_list) > 1:
            value_idx = randint(0, 1)
            for i in range(2):
                self.play_turn(available_board_values[value_idx], self.tactics[available_board_values[value_idx]])
                value_idx += 1
                value_idx %= 2
                if self.check_game_finished():
                    return True
            # selected = self.moves_list[0]
            # self.board[selected[0]][selected[1]] = r_value
            # self.moves_list = self.moves_list[1:]
            # if self.check_game_finished():
            #     return True

            if self.special_prob.draw_idx() > 0:
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
        self.tactics = {b_value: "random", r_value: "random"}
        if self.draw_prob.draw_idx() > 0:
            available_board_values = [b_value, r_value]
            value_idx = randint(0, 1)
            self.tactics[available_board_values[value_idx]] = "draw"
        finished = self.play_round()
        if verbose:
            self.print_status("finished a round")
        while not finished:
            finished = self.play_round()
            if verbose:
                self.print_status("finished a round")
        return self.winner
    def print_status(self, header=""):
        msg = """__________\n{header}\ntactic: {tactic}\nwinner: {winner}\nmoves:\n{moves}\nboard:\n{board}""".format(
            tactic = str(self.tactics), winner = str(self.winner), moves = str(self.moves_list),
                          board = str(self.board), header = str(header))
        print(msg)
