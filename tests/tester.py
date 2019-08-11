import pytest

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
    fn = "tests/data/1sudoku.txt"
    boards = load_sudoku_boards(fn)
    assert(len(boards)==1)
    return boards[0]


# happy path
def test_1sudoku():
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
    solver.solve()
    assert(single_board==expected_solution)


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
