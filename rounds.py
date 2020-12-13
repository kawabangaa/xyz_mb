import numpy as np
from constants import animal_cnt
from constants import b_value, r_value, d_value, verbose


def invoke_animal(board, moves, animal_prob):
    animal_idx = animal_prob.draw_idx()
    animal_cnt[animal_idx] += 1
    if verbose:
        print("invoked: "+ str(animal_idx))
    animal_list = [wasp, chameleon, snake,cheetah]
    ret_board, ret_moves = animal_list[animal_idx](board, moves)
    return ret_board, ret_moves

def wasp(board, moves):
    # shift rows up with wrap around
    wasp_permu = {'00': '10','01':'11','02':'12','10':'20','11':'21','12':'22','20':'00', '21':'01', '22':'02'}
    return permutate_board(board, moves, wasp_permu)


def chameleon(board, moves):
    # flip 1s to -1s and the other way
    return board * -1, moves

def snake(board, moves):
    # counter clockwise turn
    snake_perm = {'00': '01', '01': '02', '02': '12', '10': '00', '11': '11', '12': '22', '20': '10', '21': '20',
                  '22': '21'}
    return permutate_board(board, moves, snake_perm)

def cheetah(board, moves):
    cheetah_moves = [b_value, b_value, r_value, r_value]
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
    B_WON = 3 * b_value
    R_WON = 3 * r_value
    values = np.append(
        np.append(board.sum(axis=0),
                  board.sum(axis=1)),
        [board[0][0] + board[1][1] + board[2][2],
         board[0][2] + board[1][1] + board[2][0]])
    winner = None
    ret = False
    for value in values:
        if value == B_WON:
            winner = b_value
            ret = True
        elif value == R_WON:
            winner = r_value
            ret = True
    if (not ret) and (not (d_value in board)):
        winner = d_value
        ret = True
    return ret, winner


