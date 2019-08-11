import os
import sys
import re
import logging
import argparse
import traceback
import statistics
from collections import defaultdict, namedtuple
from timeit import default_timer as timer

from pprint import pprint

UNSOLVED = '0'
BOARD_SIDE = 9
BOX_SIDE = 3


class SudokuSolver:
    def __init__(self, board):
        """Sudoku Solver

        Args:
            board (List[List[str]]): Sudoku board
        """
        self.board = board
        self.peers = self.precompute_peers()
        self.candidates = self.precompute_candidates()
        logging.debug(f"precomputed candidates {self.candidates}")

    def solve(self):
        pos = self.find_unsolved_cell()
        if pos is None:
            return True

        for candidate in self.candidates[pos]:
            logging.debug(f"solving for candidate {candidate} at pos {pos}")
            deleted_candidates = defaultdict(list)
            if self.is_valid(pos, candidate, deleted_candidates):
                self.board[pos[0]][pos[1]] = candidate
                if self.solve():
                    return True
            logging.debug(f"backtracking at candidate {candidate} for pos {pos}")
            self.backtrack(deleted_candidates)
        return False

    def find_unsolved_cell(self):
        """Get unsolved cells in order of least # of candidates

        Returns:
            Tuple[int, int]: position of unsolved cell, or None if all are solved
        """
        if len(self.candidates) == 0:
            return None
        return min(self.candidates.keys(), key=lambda i: len(self.candidates[i]))

    def is_valid(self, pos, candidate, deleted_candidates):
        """Checks if candidate is a valid for the cell

        Logic: 
            if candidate assignment causes any peers to have 0 candidates,
            candidate is not valid and we need to backtrack

        Args:
            pos (Tuple[int, int]): cell position
            candidate (str): candidate value for cell
            deleted_candidates (Dict[Tuple[int, int], List[str]]): deleted candidates

        Returns:
            bool: if candidate valid for cell
        """
        # store deleted candidates in case we need to backtrack
        deleted_candidates[pos].extend(self.candidates[pos])
        del self.candidates[pos]
        
        # remove candidate from peers' candidates
        for peer in self.peers[pos]:
            if peer not in self.candidates: # already solved
                continue

            if candidate in self.candidates[peer]:
                deleted_candidates[peer].append(candidate)
                self.candidates[peer].remove(candidate)

                # backtracking trigger
                if len(self.candidates[peer]) == 0:
                    return False
        return True

    def backtrack(self, deleted_candidates):
        """Backtrack and put back candidates for consideration

        Args:
            deleted_candidates (Dict[Tuple[int, int], List[str]]): deleted candidates
        """
        for pos, candidates in deleted_candidates.items():
            self.candidates[pos].extend(candidates)

    def precompute_candidates(self):
        """Precompute candidates for each cell

        Logic:
            Initially each cell has 9 candidates (1-9)
            Remove candidates based on values of peers on initial board

        Args:
            board (List[List[str]]): Sudoku board

        Returns:
            Dict[Tuple[int, int], List[str]]: valid_coordinates for each Coord
        """
        candidates = defaultdict(list)
        solved = defaultdict(list)
        for i in range(BOARD_SIDE):
            for j in range(BOARD_SIDE):
                val = self.board[i][j]
                if val == UNSOLVED:
                    candidates[(i, j)] = [str(n) for n in range(1, BOARD_SIDE+1)]
                else:
                    solved[(i, j)] = val

        for solved_pos, val in solved.items():
            for peer in self.peers[solved_pos]:
                if peer in candidates and val in candidates[peer]:
                    candidates[peer].remove(val)

        return candidates

    def precompute_peers(self):
        """Precompute peers for easy lookup

        Returns:
            Dict[Tuple[int,int], List[Tuple[int, int]]
        """
        peers = defaultdict(list)
        for r in range(BOARD_SIDE):
            for c in range(BOARD_SIDE):
                for i in range(BOARD_SIDE):
                    for j in range(BOARD_SIDE):
                        if are_peers((r, c), (i, j)):
                            peers[(r, c)].append((i, j))
        return peers


def are_peers(p1, p2):
    if p1 == p2:
        return False

    return (
        (p1[0]//BOX_SIDE, p1[1]//BOX_SIDE) == (p2[0]//BOX_SIDE, p2[1]//BOX_SIDE)  # same box
        or p1[0] == p2[0]  # same row
        or p1[1] == p2[1]  # same column
    )


def board_to_str(bo):
    s = ""
    for i in range(len(bo)):
        if i % BOX_SIDE == 0 and i != 0:
            s += "-----------------------\n"

        for j in range(len(bo[0])):
            if j % BOX_SIDE == 0 and j != 0:
                s += " | "

            if j == BOARD_SIDE-1:
                s += bo[i][j] + "\n"
            else:
                s += bo[i][j] + " "
    return s


def init_board():
    return [['0' for x in range(9)] for y in range(9)]


def str_to_board(s):
    board = init_board()
    
def load_all_sudoku_boards(boards_fn):
    """Assumptions about board txt file..."""
    all_boards = []
    try:
        with open(boards_fn) as rf:
            text = rf.read()
    except FileNotFoundError as fe:
        print(f"FileNotFoundError: {fe}")

    boards = re.split(r"Grid \d\d", text)
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


if __name__=="__main__":

    boards = load_all_sudoku_boards('tests/sudokutest.txt')
    logging.basicConfig(level=logging.INFO)
    
    t = []
    for i, board in enumerate(boards):
        logging.info(f"Grid {i+1}")
        logging.info(f"Unsolved board: \n{board_to_str(board)}")
        start = timer()
        try:
            solver = SudokuSolver(board)
            solver.solve()
        except Exception as e:
            logging.error(traceback.format_exc())
        end = timer()
        logging.info(f"Solved board: \n{board_to_str(board)}")
        t.append(end - start)

    logging.info(f"Mean (s): {statistics.mean(t)}")
    logging.info(f"STD (s): {statistics.stdev(t)}")
    logging.info(f"Total (s): {sum(t)}")
