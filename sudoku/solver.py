import os
import sys
import re
import logging
import argparse
import statistics
from collections import defaultdict
from timeit import default_timer as timer

UNSOLVED = '0'
BOARD_SIDE = 9
BOX_SIDE = 3
BOARD_DELIM_REGEX = "Grid \d\d\n"
LOG_FILE = "log.info"

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO,
    filename=LOG_FILE,
)


class SudokuSolver:
    def __init__(self, board):
        """Sudoku Solver

        Args:
            board (List[List[str]]): Sudoku board
        """
        self.board = board
        self.peers = self.precompute_peers()
        
        # existence of a cell position in self.candidates indicates cell is unsolved
        self.candidates = self.precompute_candidates()

    def solve(self):
        pos = self.find_unsolved_cell()
        if pos is None:
            return True

        for candidate in self.candidates[pos]:
            deleted_candidates = defaultdict(list)
            if self.is_valid(pos, candidate, deleted_candidates):
                self.board[pos[0]][pos[1]] = candidate
                if self.solve():
                    return True

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
        """Checks if candidate is valid for the cell position

        Logic: 
            if candidate assignment for pos causes any peers to reduce to 0 candidates,
            candidate for pos is not valid and requires backtracking

        Args:
            pos (Tuple[int, int]): cell position
            candidate (str): candidate value for cell
            deleted_candidates (Dict[Tuple[int, int], List[str]])

        Returns:
            bool: if candidate is valid for the cell
        """
        # store deleted candidates in case we need to backtrack
        deleted_candidates[pos].extend(self.candidates[pos])
        del self.candidates[pos]
        
        # remove candidate from peers' candidates
        for peer in self.peers[pos]:
            if peer not in self.candidates: # already solved cell
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
            deleted_candidates (Dict[Tuple[int, int], List[str]])
        """
        for pos, candidates in deleted_candidates.items():
            self.candidates[pos].extend(candidates)

    def precompute_candidates(self):
        """Precompute candidates for each cell

        Logic:
            Initially each unsolved cell has 9 candidates (1-9)
            Remove candidates based on values of peers on initial board

        Args:
            board (List[List[str]])

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
    """Boolean method to check if 2 positions are peers

    Args:
        p1 (Tuple[int, int])
        p2 (Tuple[int, int])
    
    Returns:
        bool: if peers
    """
    if p1 == p2:
        return False

    return (
        (p1[0]//BOX_SIDE, p1[1]//BOX_SIDE) == (p2[0]//BOX_SIDE, p2[1]//BOX_SIDE)  # same box
        or p1[0] == p2[0]  # same row
        or p1[1] == p2[1]  # same column
    )


def board_to_str(board):
    """Convert board to a string resembling a Sudoku board

    Args:
        board (List[List[str]])
    
    Returns:
        str
    """
    s = ""
    for i in range(len(board)):
        if i % BOX_SIDE == 0 and i != 0:
            s += "-----------------------\n"

        for j in range(len(board[0])):
            if j % BOX_SIDE == 0 and j != 0:
                s += " | "

            if j == BOARD_SIDE-1:
                s += board[i][j] + "\n"
            else:
                s += board[i][j] + " "
    return s


def init_board():
    """Initialize unsolved board

    Returns:
        List[List[str]]
    """
    return [[UNSOLVED for x in range(BOARD_SIDE)] for y in range(BOARD_SIDE)]


def load_all_sudoku_boards(boards_fn):
    """Load sudoku boards

    We assume the following format:
        Grid 01
        003020600
        900305001
        001806400
        008102900
        700000008
        006708200
        002609500
        800203009
        005010300
        Grid 02
        200080300
        060070084
        030500209
        000105408
        000000000
        402706000
        301007040
        720040060
        004010003
    * 9x9 grids
    * Each row a consecutive set of characters
    * Delimited by "Grid XX\n"
    
    Args:
        boards_fn (str): path to txt file containing above Grid data
    
    Returns:
        List[List[List[str]]]: list of boards
    """
    boards = []

    with open(boards_fn) as rf:
        text = rf.read()

    board_strings = filter(None, re.split(BOARD_DELIM_REGEX, text))
    for bs in board_strings:
        boards.append(str_to_board(bs.strip()))
    return boards


def str_to_board(s):
    """Convert a string of the following format:
        200080300
        060070084
        030500209
        000105408
        000000000
        402706000
        301007040
        720040060
        004010003
       to a board
    
    Args:
        s (str)
    
    Returns:
        List[List[str]]: board
    """
    board = init_board()
    lines = s.split("\n")
    for row, line in enumerate(s.strip().split("\n")):
        board[row] = list(line)
    return board


if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--boards_file", default="sudoku.txt")
    args = p.parse_args()

    try:
        boards = load_all_sudoku_boards(args.boards_file)
    except:
        logging.error(f"Error loading {args.boards_file}. Exiting...", exc_info=True)
        sys.exit(1)

    t = []
    for i, board in enumerate(boards):
        logging.info(f"Grid {i+1}")
        try:
            logging.info(f"Unsolved board: \n{board_to_str(board)}")
            start = timer()
        
            solver = SudokuSolver(board)
            solver.solve()
            end = timer()
            logging.info(f"Solved board: \n{board_to_str(board)}")
            t.append(end - start)
        except:
            logging.error(f"Error processing Grid {i+1}", exc_info=True)

    try:
        logging.info(f"Mean (s): {statistics.mean(t)}")
        logging.info(f"STD (s): {statistics.stdev(t)}")
        logging.info(f"Total (s): {sum(t)}")
    except:
        logging.error("Error computing statistics", exc_info=True)