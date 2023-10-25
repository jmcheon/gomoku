from Board import Board
from config import *
from doublethree import is_valid_position


directions = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]


def dfs_capture(board: Board, x, y, player, direction, count):
    nx = x + direction[0]
    ny = y + direction[1]

    if count == 3:
        if is_valid_position((nx, ny)) == True and board.get_value(nx, ny) == player:
            return True
        else:
            return False

    if not is_valid_position((nx, ny)):
        return False
    if board.get_value(nx, ny) != (PLAYER2 if player == PLAYER1 else PLAYER1):
        return False

    return dfs_capture(board, nx, ny, player, direction, count + 1)


def capture_opponent(board: Board, x, y, player):
    print("capture_opponent", (x, y), player)
    captured_list = []
    for dir in directions:
        print(dir)
        if dfs_capture(board, x, y, player, dir, 1) == True:
            captured_list.append(((x, y), dir))
            print("stone pairs found!")

    print(captured_list)
