import os
import sys
import argparse
from collections import namedtuple, defaultdict
from pprint import pprint
import copy
UNSOLVED_VALUE = '0'

Coord = namedtuple('Coord', ['row', 'col'])

def init_board():
    return [['0' for x in range(9)] for y in range(9)]

def load_all_sudoku_boards(boards_fn):
    """Assumptions about board txt file..."""
    all_boards = []
    try:
        with open(boards_fn) as rf:
            lines = rf.readlines()
    except FileNotFoundError as fe:
        print(f"FileNotFoundError: {fe}")

    board = init_board()
    for i, line in enumerate(lines):
        row = i%10-1
        if i==0: 
            continue
        if i%10==0:
            all_boards.append(board)
            board = init_board()
            continue
        board[row] = list(line.strip())
    all_boards.append(board)
    return all_boards

class SudokuSolver():
    def __init__(self, board):
        """Sudoku Solver

        Assumptions:
            9x9 board

        Args:
            board (List[List[str]]): Sudoku board
        """
        self.board = board
        self.candidates = self.precompute_candidates()
        self.peers = self.precompute_peers()
        # pprint(self.candidates)

    def solve(self):
        """
        Args:
            board (List[List[str]]): Sudoku board
        Returns:
            bool
        """
        pos = self.find_unsolved_cell()
        if pos is None:
            return True

        for candidate in self.candidates[pos]:
            save_state = copy.deepcopy(self.candidates)
            # print(f"solving for candidate {candidate} at pos {pos}")
            if self.is_valid(pos, candidate):
                self.board[pos[0]][pos[1]] = candidate
                if self.solve():
                    return True

            self.undo(save_state)
        return False

    def find_unsolved_cell(self):
        if len(self.candidates)==0:
            return None
        return min(self.candidates.keys(), key=lambda i: len(self.candidates[i]))

    def is_valid(self, pos, candidate):
        """Update peers' valid_candidates
        If peer valid_candidates goes to None, return False, else return True
        Args:
            candidate
            valid_candidates
            board
        
        Returns:
            bool: if unsuccessful candidate removal b/c empty list
        """
        # print(f"deleting pos: {pos}")
        del self.candidates[pos]
        for peer in self.peers[pos]:
            if peer not in self.candidates:
                continue

            # print(f"deleting candidate {candidate} from peer {peer}")
            if candidate in self.candidates[peer]:
                self.candidates[peer].remove(candidate)
                if len(self.candidates[peer])==0:
                    # pprint(self.candidates)
                    # print("returning False")
                    return False
        return True

    def undo(self, saved_state):
        # print(f"putting back deleted_candidates: {deleted_candidates}")
        self.candidates = saved_state
        # for pos in deleted_candidates:
            # self.candidates[pos].append(deleted_candidates[pos])

    def precompute_candidates(self):
        """
        Args:
            board (List[List[str]]): Sudoku board
        Returns:
            Dict[Tuple[int, int], List[str]]: valid_coordinates for each Coord
        """
        a = "123456789"
        d = {}
        val = defaultdict(list)
        for i in range(9):
            for j in range(9):
                ele = board[i][j]
                if ele != "0":
                    d[("r", i)] = d.get(("r", i), []) + [ele]
                    d[("c", j)] = d.get(("c", j), []) + [ele]
                    d[(i//3, j//3)] = d.get((i//3, j//3), []) + [ele]
                else:
                    val[(i,j)] = []
        for (i,j) in val.keys():
            inval = d.get(("r",i),[])+d.get(("c",j),[])+d.get((i//3,j//3),[])
            val[(i,j)] = [n for n in a if n not in inval ]
        return val

    def precompute_peers(self):
        peers = defaultdict(list)
        for r in range(len(self.board[0])):
            for c in range(len(self.board[1])):
                for i in range(len(self.board[0])):
                    for j in range(len(self.board[1])):
                        if are_peers((r,c), (i,j)):
                            peers[(r,c)].append((i,j))
        return peers

def are_peers(p1, p2):
    if p1 == p2:
        return False

    return (
        (p1[0]//3, p1[1]//3) == (p2[0]//3, p2[1]//3) # same box
        or p1[0] == p2[0] # same row
        or p1[1] == p2[1] # same column
    )

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

import time
if __name__=="__main__":

    boards = load_all_sudoku_boards('sudoku.txt')

    # print(len(boards))
    # print(boards[-1])
    # sys.exit(1)
    start = time.time()
    for i, board in enumerate(boards):
        print(i)
        print("before")
        print_board(board)
        solver = SudokuSolver(board)
        solver.solve()
        print("after")
        print_board(board)
        # sys.exit(1)

    end = time.time()
    print(end - start)