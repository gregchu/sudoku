import os
import sys
import argparse
from collections import namedtuple, defaultdict
from pprint import pprint
import copy

UNSOLVED_VALUE = '0'

Coord = namedtuple('Coord', ['row', 'col'])

BOARD_SIDE = 9
BOX_SIDE = 3

def init_board():
    return [['0' for x in range(9)] for y in range(9)]

def load_all_sudoku_boards(boards_fn):
    """Assumptions about board txt file..."""
    all_boards = []
    lines = []
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
        self.peers = self.precompute_peers()
        self.candidates = self.precompute_candidates()
        
        # pprint(self.candidates)

    def solve(self):
        """
        Args:
            board (List[List[str]]): Sudoku board
        Returns:
            bool
        """
        pos = self.find_unsolved_cell()
        print(f'find unsolved cell pos: {pos}')
        if pos is None:
            return True

        for candidate in self.candidates[pos]:
            print(f"solving for candidate {candidate} at pos {pos}")
            # pprint(self.candidates)
            deleted_candidates = defaultdict(list)
            # print('update: {}'.format(deleted))
            if self.is_valid(pos, candidate, deleted_candidates):
                self.board[pos[0]][pos[1]] = candidate
                if self.solve():
                    return True
            print(f"about to call undo at candidate {candidate} for pos {pos}")
            self.backtrack(pos, deleted_candidates)
        return False

    def find_unsolved_cell(self):
        if len(self.candidates)==0:
            return None
        return min(self.candidates.keys(), key=lambda i: len(self.candidates[i]))

    def is_valid(self, pos, candidate, deleted_candidates):
        """Update peers' valid_candidates
        If peer valid_candidates goes to None, return False, else return True
        Args:
            candidate
            valid_candidates
            board
        
        Returns:
            bool: if unsuccessful candidate removal b/c empty list
        """
        print(f"deleting pos: {pos}")
        pprint(deleted_candidates)
        deleted_candidates[pos].extend(self.candidates[pos])
        del self.candidates[pos]
        for peer in self.peers[pos]:
            if peer not in self.candidates:
                continue

            if candidate in self.candidates[peer]:
                print(f"deleting candidate {candidate} from peer {peer}")
                # deleted[peer] = candidate
                deleted_candidates[peer].append(candidate)
                print("deleted_stack:")
                pprint(deleted_candidates)
                # pprint(deleted)
                self.candidates[peer].remove(candidate)
                
                if len(self.candidates[peer])==0:
                    print(f"empty candidate list for peer pos: {peer}")
                    pprint(self.candidates)
                    print("returning False")
                    pprint(deleted_candidates)
                    return False
        return True

    def backtrack(self, pos, deleted_candidates):
        print("undoing: pos: {} update: {}".format(pos, deleted_candidates))
        
        # for pos, candidates in
        # for item in deleted_stack:
        #     print(item.keys())
        #     self.candidates[item.keys()[0]].extend(item.values)
        for pos, candidates in deleted_candidates.items():
            self.candidates[pos].extend(candidates)
        # for k in deleted:
        #     if k not in self.candidates:
        #         self.candidates[k] = deleted[k]
        #     else:
        #         self.candidates[k].append(deleted[k])
        return None
        # print(f"putting back deleted_candidates: {deleted_candidates}")
        # self.candidates = saved_state
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
        # p = [str(i) for i in range(1, BOARD_SIDE+1)]
# d = {}
        candidates = defaultdict(list)
        solved = defaultdict(list)
        # board = {}
        for i in range(9):
            for j in range(9):
                ele = board[i][j]
                if ele == "0":
                    # d[("r", i)] = d.get(("r", i), []) + [ele]
                    # d[("c", j)] = d.get(("c", j), []) + [ele]
                    # d[(i//3, j//3)] = d.get((i//3, j//3), []) + [ele]
                # else:
                    candidates[(i,j)] = [str(n) for n in range(1, 10)]
                else:
                    solved[(i,j)] = ele
                # else: #unsolved
                    # val[(i,j)] = []
                # print(f'd for (i,j) ({i}, {j})')
                # pprint(d)
        # pprint(d)
        # print(len(d))
        # for 
        pprint(candidates)
        print(len(candidates))
        for spos, val in solved.items():
            for peer in self.peers[spos]:
                if peer in candidates and val in candidates[peer]:
                    candidates[peer].remove(val)
        
        # for pos, cans in candidates.items():

        #     for can in cans:
        #         if not _valid(self.board, can, pos):
        #             print(f'removing {can} from pos {pos}')
        #             candidates[pos].remove(can)
        #             # pprint(candidates)
        pprint(candidates)
        print(len(candidates))
        # for (i,j) in val.keys():
        #     inval = d.get(("r",i),[])+d.get(("c",j),[])+d.get((i//3,j//3),[])
        #     val[(i,j)] = [n for n in a if n not in inval ]
        # pprint(val)
        return candidates

    def precompute_peers(self):
        peers = defaultdict(list)
        for r in range(len(self.board[0])):
            for c in range(len(self.board[1])):
                for i in range(len(self.board[0])):
                    for j in range(len(self.board[1])):
                        if are_peers((r, c), (i, j)):
                            peers[(r, c)].append((i, j))
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
            print("--------------------")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")
    
import time
if __name__=="__main__":

    boards = load_all_sudoku_boards('sudokutest.txt')

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
        sys.exit(1)

    end = time.time()
    print(end - start)