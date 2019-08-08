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
    return all_boards

class SudokuSolver():
    def solve(self, board):
        """
        Args:
            board (List[List[str]]): Sudoku board
        """
        self.board = board
        self.valid_candidates = self.precompute_valid_candidates()
        pprint(self.valid_candidates)
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

    def _solve(self):
        """
        Args:
            board (List[List[str]]): Sudoku board

        Returns:
            bool
        """
        if len(self.valid_candidates)==0:
            return True # base case

        coord = min(self.valid_candidates.keys(), key=lambda x: len(self.valid_candidates[x]))

        for candidate in self.valid_candidates[coord]:
            pprint(self.valid_candidates)
            print(f'checking to delete candidate: {candidate}')
            deleted = {coord: self.valid_candidates[coord]}
            print(f'deleted: {deleted}')
            self.board[coord[0]][coord[1]] = candidate
            del self.valid_candidates[coord]
            if self.is_valid_update_peers(candidate, coord, deleted):
                pprint(self.valid_candidates)
                # sys.exit(1)
                if self._solve():
                    return True

            # undo and try again
            self.board[coord[0]][coord[1]] = UNSOLVED_VALUE
            self.put_back(coord, deleted)
        return False


    def is_valid_update_peers(self, candidate, coord, update):
        """Update peers' valid_candidates

        If peer valid_candidates goes to None, return False, else return True

        Args:
            candidate
            valid_candidates
            board
        
        Returns:
            bool
        """
        r, c = coord
        for coord in self.valid_candidates.keys():
            if candidate in self.valid_candidates[coord]:
                if coord[0]==r or coord[1]==c or (coord[0]/3, coord[1]/3)==(r/3,c/3):
                    update[coord] = candidate
                    print(f"removing {candidate} from coord: {coord} with vals {self.valid_candidates[coord]}")
                    self.valid_candidates[coord].remove(candidate)
                    pprint(self.valid_candidates)
                    if len(self.valid_candidates[coord])==0:
                        print("returning False")
                        print_board(board)
                        return False
        return True

    def put_back(self, coord, deleted):
        pprint(self.valid_candidates)
        print(f"undoing: key: {coord} update: {deleted}")
        for coord in deleted:
            if coord not in self.valid_candidates:
                self.valid_candidates[coord] = deleted[coord]
            else:
                self.valid_candidates[coord].append(deleted[coord])
        # print_board(self.board)
        pprint(self.valid_candidates)
class Solver():
    def solve(self, board):
        """
        Args:
            board (List[List[str]])
        """
        self.board = board
        self.valid_candidates = self.compute_candidates()
        pprint.pprint(self.valid_candidates)
        sys.exit(1) 
        self._solve()
    
    def compute_candidates(self):
        # a = "123456789"
        # d, val = {}, {}
        # for i in range(9):
        #     for j in range(9):
        #         ele = self.board[i][j]
        #         if ele != "0":
        #             d[("r", i)] = d.get(("r", i), []) + [ele]
        #             d[("c", j)] = d.get(("c", j), []) + [ele]
        #             d[(i//3, j//3)] = d.get((i//3, j//3), []) + [ele]
        #         else:
        #             val[Coord(i,j)] = []
        # # for k, v in d.items():
        # #     print(k, v)
        # for c in val.keys():
        #     inval = d.get(("r", c.row),[])+d.get(("c", c.col),[])+d.get((c.row/3,c.col/3),[])
        #     val[Coord(i,j)] = [n for n in a if n not in inval ]
        # return val
        a = "123456789"
        d, val = {}, {}
        for i in range(9):
            for j in range(9):
                ele = self.board[i][j]
                if ele != "0":
                    d[("r", i)] = d.get(("r", i), []) + [ele]
                    d[("c", j)] = d.get(("c", j), []) + [ele]
                    d[(i//3, j//3)] = d.get((i//3, j//3), []) + [ele]
                else:
                    val[(i,j)] = []
        # for k, v in d.items():
        #     print(k, v)
        for (i,j) in val.keys():
            inval = d.get(("r",i),[])+d.get(("c",j),[])+d.get((i/3,j/3),[])
            val[(i,j)] = [n for n in a if n not in inval ]
        return val

    def _solve(self):
        if not self.candidates_per_coord:
            return True #base case
        print('VAL')
        pprint.pprint(self.valid_candidates)
        key = min(self.valid_candidates.keys(), key=lambda x: len(self.valid_candidates[x]))
        print(key)
        for candidate in self.valid_candidates[key]:
            print(f'checking to delete n: {n}')
            update = {kee:self.valid_candidates[kee]}
            if self.ValidOne(n, kee, update): # valid choice
                if self._solve(): # keep solving
                    return True
            self.undo(kee, update) # invalid choice or didn't solve it => undo
        return False

    def ValidOne(self, n, kee, update):
        self.board[kee[0]][kee[1]] = n
        print(f'deleting: {self.candidates_per_coord[kee]}')
        del self.valid_candidates[kee] #better than del pattern?
        i, j = kee
        for ind in self.candidates_per_coord.keys():
            if n in self.candidates_per_coord[ind]:
                if ind[0]==i or ind[1]==j or (ind[0]/3,ind[1]/3)==(i/3,j/3):
                    update[ind] = n
                    print(f"removing {n} from coord: {ind} with vals {self.candidates_per_coord[ind]}")
                    self.candidates_per_coord[ind].remove(n)
                    if len(self.candidates_per_coord[ind])==0:
                        print("returning False")
                        print_board(self.board)
                        return False
        return True

    def undo(self, kee, update):
        pprint.pprint(self.candidates_per_coord)
        print(f"undoing: key: {kee} update: {update}")
        #self.board[kee[0]][kee[1]]="xx"
        for k in update:            
            if k not in self.candidates_per_coord:
                self.candidates_per_coord[k]= update[k]
            else:
                self.candidates_per_coord[k].append(update[k])
        # print_board(self.board)
        pprint.pprint(self.candidates_per_coord)
        return None

def print_board(board):
    for b in board:
        print(b)

import time
if __name__=="__main__":

    boards = load_all_sudoku_boards('sudoku.txt')

    start = time.time()
    for i, board in enumerate(boards):
        print(i)
        print("before")
        print_board(board)
        solver = SudokuSolver()
        solver.solve(board)
        print("after")
        print_board(board)
        sys.exit(1)

    end = time.time()
    print(end - start)
