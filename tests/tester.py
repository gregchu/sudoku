import pytest
from collections import defaultdict

from sudoku.solver import (
    str_to_board, 
    load_sudoku_boards,
    SudokuSolver,
    are_peers,
    precompute_candidates,
    precompute_peers,
)


# input loading
def test_smaller_input_size():
    fn = "tests/data/smaller_input.txt"
    with pytest.raises(AssertionError):
        boards = load_sudoku_boards(fn)


def test_larger_input_size():
    fn = "tests/data/larger_input.txt"
    with pytest.raises(AssertionError):
        boards = load_sudoku_boards(fn)


def test_larger_input_size2():
    fn = "tests/data/larger_input2.txt"
    with pytest.raises(AssertionError):
        boards = load_sudoku_boards(fn)


def test_char_input():
    fn = "tests/data/haschar.txt"
    with pytest.raises(ValueError):
        boards = load_sudoku_boards(fn)


def test_delimiter_input():
    fn = "tests/data/delimiter.txt"
    with pytest.raises(AssertionError):
        boards = load_sudoku_boards(fn)


def load_board():
    fn = "tests/data/sudoku1.txt"
    boards = load_sudoku_boards(fn)
    assert(len(boards)==1)
    return boards[0]


# helper functions
def test_are_peers():
    p1 = (2, 2)
    p2 = (2, 3)
    p3 = (3, 3)
    assert are_peers(p1, p2)
    assert are_peers(p2, p3)
    with pytest.raises(AssertionError):
        assert are_peers(p1, p3) # different boxes


def test_precompute_peers():
    peers = precompute_peers()
    # test just a few 
    assert (2, 2) in peers[(0, 0)]
    assert (0, 1) in peers[(0, 0)]
    assert ((3, 3) in peers[(0, 0)]) is False


def test_precompute_candiates():
    single_board = load_board()
    peers = precompute_peers()
    candidates = precompute_candidates(single_board, peers)
    # test just a few
    assert candidates[(7, 5)] == [1, 8]
    assert candidates[(7, 8)] == [1, 9]
    assert candidates[(2, 4)] == [1, 2, 4, 5, 7, 8]


# happy path
def test_solve():
    single_board = load_board()
    expected_solution = [
        [2, 9, 4, 8, 6, 3, 5, 1, 7], 
        [7, 1, 5, 4, 2, 9, 6, 3, 8], 
        [8, 6, 3, 7, 5, 1, 4, 9, 2], 
        [1, 5, 2, 9, 4, 7, 8, 6, 3], 
        [4, 7, 9, 3, 8, 6, 2, 5, 1], 
        [6, 3, 8, 5, 1, 2, 9, 7, 4], 
        [9, 8, 6, 1, 3, 4, 7, 2, 5], 
        [5, 2, 1, 6, 7, 8, 3, 4, 9], 
        [3, 4, 7, 2, 9, 5, 1, 8, 6]
    ]
    solver = SudokuSolver(single_board)
    assert solver.solve()
    assert single_board == expected_solution


def test_find_unsolved_cell():
    single_board = load_board()
    solver = SudokuSolver(single_board)
    pos = solver.find_unsolved_cell()
    expected = (0, 3)
    assert pos == expected


def test_find_unsolved_cell_on_solved_board():
    solved = [
        [2, 9, 4, 8, 6, 3, 5, 1, 7], 
        [7, 1, 5, 4, 2, 9, 6, 3, 8], 
        [8, 6, 3, 7, 5, 1, 4, 9, 2], 
        [1, 5, 2, 9, 4, 7, 8, 6, 3], 
        [4, 7, 9, 3, 8, 6, 2, 5, 1], 
        [6, 3, 8, 5, 1, 2, 9, 7, 4], 
        [9, 8, 6, 1, 3, 4, 7, 2, 5], 
        [5, 2, 1, 6, 7, 8, 3, 4, 9], 
        [3, 4, 7, 2, 9, 5, 1, 8, 6]
    ]
    solver = SudokuSolver(solved)
    pos = solver.find_unsolved_cell()
    assert pos is None


def test_is_valid():
    single_board = load_board()
    solver = SudokuSolver(single_board)
    # valid candidates for pos (0, 3) are [4, 8]
    deleted_candidates = defaultdict(list)
    assert solver.is_valid((0, 3), 3, deleted_candidates) is False
    assert solver.is_valid((0, 3), 4, deleted_candidates)


def test_backtrack():
    single_board = load_board()
    solver = SudokuSolver(single_board)
    deleted_candidates = {
        (6, 5): [5], 
        (6, 8): [5], 
        (8, 5): [5]
    }
    solver.backtrack(deleted_candidates)
    expected = {
        (0, 0): [2, 4, 8, 9],
        (0, 1): [2, 8, 9],
        (0, 2): [2, 4, 8],
        (0, 3): [4, 8],
        (0, 4): [2, 4, 5, 6, 8],
        (0, 6): [4, 5, 6, 9],
        (1, 0): [2, 4, 7],
        (1, 3): [4, 7],
        (1, 4): [2, 4, 6, 7],
        (1, 6): [4, 6],
        (1, 7): [3, 6],
        (2, 0): [2, 4, 7, 8, 9],
        (2, 2): [2, 3, 4, 7, 8],
        (2, 3): [1, 4, 7, 8],
        (2, 4): [1, 2, 4, 5, 7, 8],
        (2, 5): [1, 2, 4, 5, 8],
        (2, 6): [4, 5, 9],
        (2, 7): [3, 5, 9],
        (2, 8): [2, 3, 5, 9],
        (3, 1): [2, 3, 5, 8],
        (3, 2): [2, 3, 4, 6, 8],
        (3, 3): [3, 4, 8, 9],
        (3, 4): [2, 3, 4, 6, 8, 9],
        (3, 6): [5, 6, 8, 9],
        (3, 7): [3, 5, 6, 8, 9],
        (3, 8): [3, 5, 6, 9],
        (4, 0): [4, 6, 7, 8],
        (4, 1): [3, 5, 7, 8],
        (4, 3): [1, 3, 4, 8],
        (4, 4): [1, 3, 4, 6, 8],
        (4, 5): [1, 4, 6, 8],
        (4, 7): [3, 5, 6, 7, 8],
        (4, 8): [1, 3, 5, 6],
        (5, 0): [2, 6, 7, 8],
        (5, 1): [2, 3, 7, 8],
        (5, 2): [2, 3, 6, 7, 8],
        (5, 4): [1, 2, 3, 6, 8, 9],
        (5, 5): [1, 2, 6, 8],
        (5, 6): [1, 6, 7, 8, 9],
        (5, 7): [3, 6, 7, 8, 9],
        (6, 0): [6, 7, 8, 9],
        (6, 1): [7, 8, 9],
        (6, 2): [1, 6, 7, 8],
        (6, 3): [1, 3, 4, 7, 8, 9],
        (6, 4): [1, 3, 4, 5, 7, 8, 9],
        (6, 5): [1, 4, 5, 8, 5],
        (6, 6): [1, 5, 6, 7, 8, 9],
        (6, 8): [1, 5, 6, 9, 5],
        (7, 1): [2, 7, 8, 9],
        (7, 2): [1, 2, 7, 8],
        (7, 4): [1, 7, 8, 9],
        (7, 5): [1, 8],
        (7, 8): [1, 9],
        (8, 2): [1, 6, 7, 8],
        (8, 4): [1, 5, 7, 8, 9],
        (8, 5): [1, 5, 8, 5],
        (8, 6): [1, 5, 6, 7, 8, 9],
        (8, 7): [5, 6, 7, 8, 9],
        (8, 8): [1, 5, 6, 9]
    }
    assert expected == solver.candidates
