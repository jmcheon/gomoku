from config import *
from src.game.board import Board

from src.game.game_util import *


def dfs(board: Board, x, y, player, direction, count, player_count):
    nx, ny = x + direction[0], y + direction[1]
    if not is_valid_position((nx, ny)) or count > 4:
        return False

    if 3 <= count and count <= 4:
        if (
            player_count >= 3
            and is_valid_position((nx, ny)) == True
            and board.get_value(nx, ny)
            != (PLAYER_2 if player == PLAYER_1 else PLAYER_1)
        ):
            return True

    if not is_valid_position((nx, ny)):
        return False

    if board.get_value(nx, ny) == (PLAYER_2 if player == PLAYER_1 else PLAYER_1):
        return False

    if board.get_value(nx, ny) == player:
        player_count += 1

    return dfs(board, nx, ny, player, direction, count + 1, player_count)


def check_next_only_range(board: Board, x, y, dir, player):
    return_list = []
    opposite_dir = (-dir[0], -dir[1])

    def is_valid_and_empty(pos):
        return is_valid_position(pos) and board.get_value(*pos) == EMPTY_SQUARE

    def check_condition(condition, *positions):
        return all(condition(pos) for pos in positions)

    if not check_condition(
        is_valid_and_empty,
        (x + dir[0], y + dir[1]),
        (x + dir[0] * 2, y + dir[1] * 2),
        (x - dir[0], y - dir[1]),
        (x - dir[0] * 2, y - dir[1] * 2),
    ):
        return None

    def process_direction(direction, opposite=False):
        nonlocal return_list
        if (
            board.get_value(x + direction[0], y + direction[1])
            == player
            == board.get_value(x - direction[0], y - direction[1])
        ):
            return_list += make_list_to_direction(
                board, x, y, direction if not opposite else opposite_dir, 3, player
            )

    if dfs(board, x, y, player, dir, 2, 2) and check_condition(
        is_valid_and_empty, (x - dir[0] * 2, y - dir[1] * 2)
    ):
        process_direction(dir)

    elif dfs(board, x, y, player, opposite_dir, 2, 2) and check_condition(
        is_valid_and_empty, (x + dir[0] * 2, y + dir[1] * 2)
    ):
        process_direction(opposite_dir, True)

    return list(set(return_list))


def check_double_three(board: Board, x, y, player):
    def find_continuous_range():
        for dir in DIRECTIONS:
            if (
                dfs(board, x, y, player, dir, 1, 1)
                and is_valid_position((x - dir[0], y - dir[1]))
                and board.get_value(x - dir[0], y - dir[1])
                != (PLAYER_2 if player == PLAYER_1 else PLAYER_1)
            ):
                return make_list_to_direction(board, x, y, dir, 5, player), dir
        return None, None

    continous_range, direction = find_continuous_range()
    if direction is None:
        for i in range(len(DIRECTIONS) // 2):
            continous_range = check_next_only_range(board, x, y, DIRECTIONS[i], player)
            if continous_range:
                direction = DIRECTIONS[i]
                break
    if direction is not None:
        directions_copy = [
            d
            for d in DIRECTIONS
            if d != direction and d != (-direction[0], -direction[1])
        ]
        for one_place in continous_range:
            for dir in directions_copy:
                if (
                    dfs(board, one_place[0], one_place[1], player, dir, 1, 1)
                    and is_valid_position(
                        (one_place[0] - dir[0], one_place[1] - dir[1])
                    )
                    and board.get_value(one_place[0] - dir[0], one_place[1] - dir[1])
                    == EMPTY_SQUARE
                ):
                    print()
                    print(one_place[0], one_place[1], dir)
                    print("double three found!!!!!!!!!!!!")
                    return True
                elif check_next_only_range(
                    board, one_place[0], one_place[1], dir, player
                ):
                    print("double three found")
                    return True
    return False
