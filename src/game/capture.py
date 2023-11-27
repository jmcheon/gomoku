from src.game.board import Board
from config import *
from game.doublethree_old import is_valid_position


directions = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]


def dfs_capture(board: Board, x, y, player, direction, count):
    nx = x + direction[0]
    if nx > NUM_LINES:
        return False
    ny = y + direction[1]
    if ny > NUM_LINES:
        return False

    if count == 3:
        if is_valid_position((nx, ny)) == True and board.get_value(nx, ny) == player:
            return True
        else:
            return False

    if not is_valid_position((nx, ny)):
        return False
    if board.get_value(nx, ny) != (PLAYER_2 if player == PLAYER_1 else PLAYER_1):
        return False

    return dfs_capture(board, nx, ny, player, direction, count + 1)


def remove_captured_list(board: Board, captured_list):
    for i in range(len(captured_list)):
        remove_pairs(board, captured_list[i])


def remove_pairs(board: Board, captured_pairs):
    (x, y), direction = captured_pairs
    nx = 0
    ny = 0
    for _ in range(2):
        nx = x + direction[0] if nx == 0 else nx + direction[0]
        ny = y + direction[1] if ny == 0 else ny + direction[1]
        board.set_value(nx, ny, EMPTY_SQUARE)


def capture_opponent(board: Board, x, y, player):
    print("capture_opponent", (x, y), player)
    captured_list = []
    for dir in directions:
        # print(dir)
        if dfs_capture(board, x, y, player, dir, 1) == True:
            captured_list.append([(x, y), dir])

    return captured_list
