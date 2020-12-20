from random import randint

import numpy as np
from constants import animal_cnt
from constants import BLACK_VALUE, RED_VALUE, DRAW_VALUE, VERBOSE,POSSIBLE_PLAYER_VALUES

BEAST_STRING = ["wasp", "chameleon", "snake", "cheetah"]

def invoke_beast(board, moves, beast_prob):
    """
    invokes a single beast on the current board. draws from the beast probability which beast is to be invoked,
    invokes it and return the modified board and list of moves.
    :param board: 3 by 3 numpy array of the current board
    :param moves: list of available moves on the current board
    :param beast_prob: the Probability class of the current beasts probabilities
    :return: the modified board and list of moves
    """
    beast_idx = beast_prob.draw_idx()
    animal_cnt[beast_idx] += 1
    if VERBOSE:
        print("invoked: " + str(BEAST_STRING[beast_idx]))
    beast_list = [wasp, chameleon, snake, cheetah]
    ret_board, ret_moves = beast_list[beast_idx](board, moves)
    return ret_board, ret_moves


def wasp(board, moves):
    """
    the wasp logic is:
    123  456
    456->789
    789  123
    :param board:
    :param moves:
    :return:
    """
    # shift rows up with wrap around
    wasp_permu = {'00': '10', '01': '11', '02': '12', '10': '20', '11': '21', '12': '22', '20': '00', '21': '01',
                  '22': '02'}
    return permutate_board(board, moves, wasp_permu)


def chameleon(board, moves):
    """
    the chameleon logic is to flip every red to black and the opposite
    :param board:
    :param moves:
    :return:
    """
    # flip 1s to -1s and the other way
    return board * -1, moves


def snake(board, moves):
    """
    the snake logic is:
    123  236
    456->159
    789  478
    :param board:
    :param moves:
    :return:
    """
    # counter clockwise turn
    snake_perm = {'00': '01', '01': '02', '02': '12', '10': '00', '11': '11', '12': '22', '20': '10', '21': '20',
                  '22': '21'}
    return permutate_board(board, moves, snake_perm)


def cheetah(board, moves):
    """
    the cheetah logic is to play two black turns and then two red turns
    :param board:
    :param moves:
    :return:
    """
    first_idx = randint(0, 1)
    second_idx = (first_idx + 1) % 2
    cheetah_moves = [POSSIBLE_PLAYER_VALUES[first_idx], POSSIBLE_PLAYER_VALUES[first_idx],
                     POSSIBLE_PLAYER_VALUES[second_idx], POSSIBLE_PLAYER_VALUES[second_idx]]
    int_board = np.copy(board)
    int_moves = np.copy(moves)
    for idx in range(min(len(int_moves), 4)):
        selected = int_moves[0]
        int_board[selected[0]][selected[1]] = cheetah_moves[idx]
        int_moves = int_moves[1:]
        done, _ = validate_board(int_board)
        if done:
            break
    return int_board, int_moves


def permutate_board(board, moves_list, permu):
    """
    implements a generic permutation on the board.
    given a needed permutation, performs it on the board and on the list of moves
    :param board:
    :param moves_list:
    :param permu:dictionary of origins as key and destination as value
    :return:
    """
    permu_board = np.copy(board)
    permu_moves = np.copy(moves_list)
    reverse_perm = {}
    for key, value in permu.items():
        reverse_perm[value] = key
        key_msb = int(key[0])
        key_lsb = int(key[1])
        val_msb = int(value[0])
        val_lsb = int(value[1])
        permu_board[key_msb][key_lsb] = board[val_msb][val_lsb]

    for idx in range(len(permu_moves)):
        key = "{:01}{:01}".format(moves_list[idx][0], moves_list[idx][1])
        permu_moves[idx] = [int(reverse_perm[key][0]), int(reverse_perm[key][1])]
    return permu_board, permu_moves


def validate_board(board):
    """
    validates a single board to see if there's a winner or a draw.
    :param board:
    :return: True if the game ended and the winner (None if none won)
    """
    B_WON = 3 * BLACK_VALUE
    R_WON = 3 * RED_VALUE
    values = np.append(
        np.append(board.sum(axis=0),
                  board.sum(axis=1)),
        [board[0][0] + board[1][1] + board[2][2],
         board[0][2] + board[1][1] + board[2][0]])
    winner = None
    ret = False
    for value in values:
        if value == B_WON:
            winner = BLACK_VALUE
            ret = True
        elif value == R_WON:
            winner = RED_VALUE
            ret = True
    if (not ret) and (not (DRAW_VALUE in board)):
        winner = DRAW_VALUE
        ret = True
    return ret, winner
