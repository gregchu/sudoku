import os
import sys
import argparse
from collections import namedtuple
from pprint import pprint

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
    def solve(self, board):
        """
        Args:
            board (List[List[str]]): Sudoku board
        """
        self.board = board
        self.valid_candidates = self.precompute_valid_candidates()
        # pprint(self.valid_candidates)
        self._solve()

    def precompute_valid_candidates(self):
        """
        Args:
            board (List[List[str]]): Sudoku board

        Returns:
            Dict[Tuple[int, int], List[str]]: valid_coordinates for each Coord
        """
        a = "123456789"
        d, val = {}, {}
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
            inval = d.get(("r",i),[])+d.get(("c",j),[])+d.get((i/3,j/3),[])
            val[(i,j)] = [n for n in a if n not in inval ]
        return val

    def get_min_coord(self):
        return min(self.valid_candidates.keys(), key=lambda i: len(self.valid_candidates[i]))

    def _solve(self):
        """
        Args:
            board (List[List[str]]): Sudoku board

        Returns:
            bool
        """
        if len(self.valid_candidates)==0:
            return True # base case

        coord = self.get_min_coord()
        for candidate in self.valid_candidates[coord]:
            self.board[coord[0]][coord[1]] = candidate
            deleted_candidates = {coord: self.valid_candidates[coord]}
            del self.valid_candidates[coord]
            if self.remove_candidate_from_peers(candidate, coord, deleted_candidates):
                if self._solve():
                    return True

            # undo and try again
            self.board[coord[0]][coord[1]] = UNSOLVED_VALUE
            self.undo_deletions(coord, deleted_candidates)
        return False


    def remove_candidate_from_peers(self, candidate, coord, deleted_candidates):
        """Update peers' valid_candidates

        If peer valid_candidates goes to None, return False, else return True

        Args:
            candidate
            valid_candidates
            board
        
        Returns:
            bool: if unsuccessful candidate removal b/c empty list
        """
        r, c = coord
        for ncoord in self.valid_candidates.keys():
            if candidate in self.valid_candidates[ncoord]:
                if are_peers(coord, ncoord):
                    deleted_candidates[ncoord] = candidate
                    self.valid_candidates[ncoord].remove(candidate)
                    if len(self.valid_candidates[ncoord])==0:
                        return False
        return True

    def undo_deletions(self, coord, deleted_candidates):
        # pprint(self.valid_candidates)
        # print(f"undoing: key: {coord} update: {deleted}")
        for coord in deleted_candidates:
            if coord not in self.valid_candidates:
                self.valid_candidates[coord] = deleted_candidates[coord]
            else:
                self.valid_candidates[coord].append(deleted_candidates[coord])
        # print_board(self.board)
        # pprint(self.valid_candidates)

def are_peers(coord1, coord2):
    return (
        (coord1[0]//3, coord1[1]//3) == (coord2[0]//3, coord2[1]//3)
        or coord1[0] == coord2[0] 
        or coord1[1] == coord2[1]
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

    print(len(boards))
    print(boards[-1])
    sys.exit(1)
    start = time.time()
    for i, board in enumerate(boards):
        print(i)
        print("before")
        print_board(board)
        solver = SudokuSolver()
        solver.solve(board)
        print("after")
        print_board(board)
        # sys.exit(1)

    end = time.time()
    print(end - start)
