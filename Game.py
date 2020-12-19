import numpy as np
from random import randint
from constants import BLACK_VALUE, RED_VALUE, DRAW_VALUE, VERBOSE
from rounds import invoke_beast, validate_board

RAND_TACTIC = "random"
DRAW_TACTIC = "draw"


class Game:

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
        """
        checks if the current game is finished (win or draw)
        sets the winner in it's variable
        :return: True if a player wins
        """
        ret, self.winner = validate_board(self.board)
        if ret:
            if VERBOSE:
                self.print_status("player {} won".format(self.winner))
        return ret

    def play_turn_rand_tactic(self, color):
        """
        play a single player turn with random tactic, based on available moves changes the board and
        deletes from the moves list
        :param color: the color of the current player's turn
        :return:
        """
        selected = self.moves_list[0]
        self.board[selected[0]][selected[1]] = color
        if len(self.moves_list) > 0:
            self.moves_list = self.moves_list[1:]
        else:
            self.moves_list = []

    def draw_tactic_row_check(self, color):
        """
        part of the draw tactic, checks if there's a row with 2 tiles marked with the opposite player color
        if so, it blocks it
        :param color: the color of the current player's turn
        :return:
        """
        # checking if in one of the rows there're 2 of the opposite color and a 0
        opposite_color = color * -1
        rows_sum = self.board.sum(axis=1)
        row_idx = np.where(rows_sum == opposite_color * 2)
        col = self.board[row_idx, :]
        if col.size > 0:
            col_idx = np.where(col.reshape((3,)) == DRAW_VALUE)
            self.board[row_idx, col_idx] = color
            self.moves_list = np.delete(self.moves_list,
                                        np.where(np.all(self.moves_list == [row_idx[0][0], col_idx[0][0]], axis=1)),
                                        axis=0)
            return

    def draw_tactic_col_check(self, color):
        """
         part of the draw tactic, checks if there's a column with 2 tiles marked with the opposite player color
        if so, it blocks it
        :param color: the color of the current player's turn
        :return:
        """
        # checking if in one of the columns there're 2 of the opposite color and a 0
        opposite_color = color * -1
        cols_sum = self.board.sum(axis=0)
        col_idx = np.where(cols_sum == opposite_color * 2)
        row = self.board[:, col_idx]
        if row.size > 0:
            row_idx = np.where(row.reshape((3,)) == DRAW_VALUE)
            self.board[row_idx, col_idx] = color
            self.moves_list = np.delete(self.moves_list,
                                        np.where(np.all(self.moves_list == [row_idx[0][0], col_idx[0][0]], axis=1)),
                                        axis=0)
            return

    def draw_tactic_diag_check(self, color):
        """
        part of the draw tactic, checks if there's a diagonal with 2 tiles marked with the opposite player color
        if so, it blocks it
        :param color: the color of the current player's turn
        :return:
        """
        # checking if in one of the diagonals there're 2 of the opposite color and a 0
        opposite_color = color * -1
        both_diag_indices = [[[0, 0], [1, 1], [2, 2]], [[0, 2], [1, 1], [2, 0]]]
        for diag_indices in both_diag_indices:
            diag_sum = 0
            for indices in diag_indices:
                diag_sum += self.board[indices[0], indices[1]]
            if diag_sum == opposite_color * 2:
                for indices in diag_indices:
                    if self.board[indices[0], indices[1]] == DRAW_VALUE:
                        self.board[indices[0], indices[1]] = color
                        self.moves_list = np.delete(self.moves_list,
                                                    np.where(np.all(self.moves_list == [indices[0], indices[1]],
                                                                    axis=1)), axis=0)
                        return

    def play_turn_draw_tactic(self, color):
        """
        main draw tactic logic. checks if any two tiles of the opposite color exists (in some row\col\diag) and blocks it
        otherwise it plays random
        :param color: the color of the current player's turn
        :return:
        """
        self.draw_tactic_row_check(color)
        self.draw_tactic_col_check(color)
        self.draw_tactic_diag_check(color)
        # else, just play random
        selected = self.moves_list[0]
        self.board[selected[0]][selected[1]] = color
        if len(self.moves_list) > 0:
            self.moves_list = self.moves_list[1:]
        else:
            self.moves_list = []

    def play_turn(self, color, tactic=RAND_TACTIC):
        """
        plays a single player turn according to the tactic (a turn is coloring a single tile of the board)
        :param color: the color of the current player's turn
        :param tactic: the tactic of the current player
        :return:
        """
        if tactic == RAND_TACTIC:
            self.play_turn_rand_tactic(color)
        elif tactic == DRAW_TACTIC:
            self.play_turn_draw_tactic(color)

    def play_round(self):
        """
        plays a single round of the game. A round is two players and a probability of a beast (or single player if it's
        the last move).
        :return:
        """
        available_board_values = [BLACK_VALUE, RED_VALUE]
        if len(self.moves_list) == 1:
            # single player plays this round
            value_idx = randint(0, 1)
            self.play_turn(available_board_values[value_idx], self.tactics[available_board_values[value_idx]])
            if VERBOSE:
                self.print_status("player {} played".format(available_board_values[value_idx]))
            if self.check_game_finished():
                return True

        elif len(self.moves_list) > 1:
            # two players play this round
            value_idx = randint(0, 1)
            for i in range(2):
                self.play_turn(available_board_values[value_idx], self.tactics[available_board_values[value_idx]])
                if VERBOSE:
                    self.print_status("player {} played".format(available_board_values[value_idx]))
                value_idx += 1
                value_idx %= 2
                if self.check_game_finished():
                    return True
            # draws a sample to decide if a special (beast) round is to be played.
            if self.special_prob.draw_idx() > 0:
                temp_board, temp_moves_list = invoke_beast(self.board, self.moves_list, self.animal_prob)
                self.board = temp_board
                self.moves_list = np.copy(temp_moves_list)
                if VERBOSE:
                    self.print_status("beast invoked")
                if self.check_game_finished():
                    return True
        else:
            if self.check_game_finished():
                return True
        return False

    def play_game(self):
        """
        plays a single game. playing rounds untill a winner is declared (or a draw)
        :return: winner value
        """
        if VERBOSE:
            self.print_status("Starting a new game, good luck")
        self.tactics = {BLACK_VALUE: RAND_TACTIC, RED_VALUE: RAND_TACTIC}
        if self.draw_prob.draw_idx() > 0:
            self.tactics = {BLACK_VALUE: DRAW_TACTIC, RED_VALUE: DRAW_TACTIC}
        finished = self.play_round()
        while not finished:
            finished = self.play_round()
        return self.winner

    def print_status(self, header=""):
        msg = """{header}\nboard:\n{board}\n_____""".format(
            board=str(self.board), header=str(header))
        print(msg)
