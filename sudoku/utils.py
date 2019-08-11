from config import BOARD_SIDE, BOX_SIDE, UNSOLVED

def are_peers(p1, p2):
    if p1 == p2:
        return False

    return (
        (p1[0] // BOX_SIDE, p1[1] // BOX_SIDE) == (p2[0] // BOX_SIDE, p2[1] // BOX_SIDE)  # same box
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
    return [[UNSOLVED for x in range(BOARD_SIDE)] for y in range(BOARD_SIDE)]


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
        row = i % BOARD_SIDE
        if i == 0:
            continue
        if i % (BOARD_SIDE+1) == 0:
            all_boards.append(board)
            board = init_board()
            continue
        board[row] = list(line.strip())
    all_boards.append(board)
    return all_boards
