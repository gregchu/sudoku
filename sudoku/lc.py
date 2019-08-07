# board = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
import sys
import json
import pprint
from collections import namedtuple

# instead of PossibleVals,
"""
use a single pass at the start
for each element
    if '0',
        add coordinate to dict
        find all the allowable values using the is_valid method on all digits

"""
Coord = namedtuple('Coord', ['r', 'c'])

class Solution:
    def solveSudoku(self, board):
        self.board = board
        self.val = self.PossibleVals()
        print(len(self.val))
        pprint.pprint(self.val)
        # sys.exit(1)
        # for k, v in self.val.items():
        #     print(k, v)
        self.Solver()

    def PossibleVals(self):
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
# USE NAMED_TUPED (ROW, COL)

    def Solver(self):
        if len(self.val)==0:
            return True #solved
        print('VAL')
        pprint.pprint(self.val)
        kee = min(self.val.keys(), key=lambda x: len(self.val[x]))
        print(kee)
        nums = self.val[kee]
        for n in nums:
            print(f'checking to delete n: {n}')
            update = {kee:self.val[kee]}
            if self.ValidOne(n, kee, update): # valid choice
                if self.Solver(): # keep solving
                    return True
            self.undo(kee, update) # invalid choice or didn't solve it => undo
        return False

    def is_member():
        pass

    def ValidOne(self, n, kee, update):
        self.board[kee[0]][kee[1]] = n
        print(f'deleting: {self.val[kee]}')
        del self.val[kee] #better than del pattern?
        i, j = kee
        for ind in self.val.keys():
            if n in self.val[ind]:
                if ind[0]==i or ind[1]==j or (ind[0]/3,ind[1]/3)==(i/3,j/3):
                    update[ind] = n
                    print(f"removing {n} from coord: {ind} with vals {self.val[ind]}")
                    self.val[ind].remove(n)
                    if len(self.val[ind])==0:
                        print("returning False")
                        return False
        return True

    def undo(self, kee, update):
        self.board[kee[0]][kee[1]]="xx"
        for k in update:            
            if k not in self.val:
                self.val[k]= update[k]
            else:
                self.val[k].append(update[k])
        return None

def print_board(board):
    for b in board:
        print(b)

def init_board():
    return [['0' for x in range(9)] for y in range(9)]

def load_euler_sudoku_boards(boards_fn):
    """Assumptions..."""
    all_boards = []
    with open(boards_fn) as rf:
        lines = rf.readlines()
    
    board = init_board()
    for i, line in enumerate(lines):
        row = i%10-1
        if i==0: 
            continue
        if i%10==0:
            # boards.append(board)
            # print(line)
            # print(board)
            all_boards.append(board)
            board = init_board()
            continue
        # board[row][:] = list(line.strip())
        # it = list(line.strip())
        # print(board[row])
        board[row] = list(line.strip())
        # for n in list(line.strip()):
        #     board[i].append(n)
        #     print(i,j)
        #     board
        # print(list(line.strip()))
        # sys.exit(1)
        # for j, c in enumerate(line):
            # board[i%10][j]= c
    
    return all_boards
import time
start = time.time()

boards = load_euler_sudoku_boards('sudoku.txt')
for i, board in enumerate(boards):
    print(i)
    print("before")
    print_board(board)
    s = Solution()
    s.solveSudoku(board)
    print("after")
    print_board(s.board)
    sys.exit(1)

end = time.time()
print(end - start)
