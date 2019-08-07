import os
import sys
import argparse
import numpy as np

N = 9
VALIDS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
EMPTY_MARKER = 0

board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True


def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None

# print_board(board)
# solve(board)
# print("___________________")
# print_board(board)


def load_boards(boards_fn):
    boards = []
    with open(boards_fn) as rf:
        lines = rf.readlines()
    
    board = np.zeros([N, N], dtype=np.int8)
    print(board)
    for i, line in enumerate(lines):
        row = i%10-1
        if i==0: 
            continue
        if i%10==0:
            # boards.append(board)
            # print(line)
            # print(board)
            boards.append(board)
            board = np.zeros([N, N], dtype=np.int8)
            continue
        board[row][:] = list(map(int, line.strip()))
        # for j, c in enumerate(line):
            # board[i%10][j]= c
    
    return boards

import time

start = time.time()
boards = load_boards("sudoku.txt")
for i, board in enumerate(boards):
    x = board.tolist()
    print_board(x)
    solve(x)
    print(i)
    print_board(x)


end = time.time()
print(end - start)

# print(9 in x)
# print(3 in x)
# if __name__=="__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("boards")
#     args = parser.parse_args()
#     boards = load_boards(args.boards)
