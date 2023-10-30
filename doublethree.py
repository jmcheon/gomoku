from Board import Board
from config import *


def is_valid_position(position):
    # Check if the position (x, y) is within the bounds of the board.
    return 0 <= position[0] < 19 and 0 <= position[1] < 19


def get_continuous_range(x, y, direction, range_num):
    test = []
    for i in range(-(range_num - 1), 1, 1):
        inside = []
        for j in range(range_num):
            if direction == EAST:
                inside.append(((x + i) + j, y))
            elif direction == NORTHEAST:
                inside.append(((x + i) + j, (y + i) + j))
            elif direction == NORTH:
                inside.append((x, (y + i) + j))
            elif direction == NORTHWEST:
                inside.append(((x - i) - j, (y + i) + j))
        test.append(inside)
    return test


def dfs(board: Board, x, y, player, direction, count, player_count):
    if count > 4:
        return False
    nx = x + direction[0]
    ny = y + direction[1]

    if 3 <= count and count <= 4:
        if (
            player_count >= 3
            and is_valid_position((nx, ny)) == True
            and board.get_value(nx, ny) != (PLAYER2 if player == PLAYER1 else PLAYER1)
        ):
            return True
        # else:
        #     return False

    if not is_valid_position((nx, ny)):
        return False

    if board.get_value(nx, ny) == (PLAYER2 if player == PLAYER1 else PLAYER1):
        return False

    if board.get_value(nx, ny) == player:
        player_count += 1

    return dfs(board, nx, ny, player, direction, count + 1, player_count)


# rework
def find_all_continuous(board: Board, x, y, player, direction):
    print("player and direction", (x, y), player, direction)
    all_list = []
    if direction == (-1, 0) or direction == (1, 0):
        for i in range(0, x):
            if board.get_value(i, y) == player:
                all_list.append((i, y))
        for i in range(x, 19):
            if board.get_value(i, y) == player:
                all_list.append((i, y))
    elif direction == (0, 1) or direction == (0, -1):
        for i in range(0, y):
            if board.get_value(x, i) == player:
                all_list.append((x, i))
        for i in range(y, 19):
            if board.get_value(x, i) == player:
                all_list.append((x, i))
    elif direction == (-1, -1) or direction == (1, 1):
        for i in range(min(x, y), 0, -1):
            if board.get_value(x - i, y - i) == player:
                all_list.append((x - i, y - i))
        all_list.append((x, y))
        for i in range(1, min(NUM_LINES - x, NUM_LINES - y)):
            if board.get_value(x + i, y + i) == player:
                all_list.append((x + i, y + i))
    elif direction == (1, -1) or direction == (-1, 1):
        for i in range(min(x, y), 0, -1):
            if board.get_value(x + i, y - i) == player:
                all_list.append((x + i, y - i))
        all_list.append((x, y))
        for i in range(1, min(NUM_LINES - x, NUM_LINES - y)):
            if board.get_value(x - i, y + i) == player:
                all_list.append((x - i, y + i))

    return all_list


def check_next_only_range(board: Board, x, y, direction, player):
    return_list = []
    if (
        is_valid_position((x + direction[0], y + direction[1])) is False
        or is_valid_position(
            (x + direction[0] + direction[0], y + direction[1] + direction[1])
        )
        is False
        or is_valid_position((x - direction[0], y - direction[1])) is False
        or is_valid_position(
            (x - direction[0] - direction[0], y - direction[1] - direction[1])
        )
        is False
    ):
        return None
    if (
        board.get_value(x, y)
        == board.get_value(x + direction[0], y + direction[1])
        == board.get_value(x - direction[0], y - direction[1])
        == player
    ) and (
        board.get_value(
            x + direction[0] + direction[0], y + direction[1] + direction[1]
        )
        != (PLAYER2 if player == PLAYER1 else PLAYER1)
        and board.get_value(
            x - direction[0] - direction[0], y - direction[1] - direction[1]
        )
        != (PLAYER2 if player == PLAYER1 else PLAYER1)
    ):
        if (
            board.get_value(
                x + direction[0] + direction[0], y + direction[1] + direction[1]
            )
            == player
        ):
            return_list.append(
                x + direction[0] + direction[0], y + direction[1] + direction[1]
            )
        elif (
            board.get_value(
                x - direction[0] - direction[0], y - direction[1] - direction[1]
            )
            == player
        ):
            return_list.append(
                (x - direction[0] - direction[0], y - direction[1] - direction[1])
            )
        return_list.append((x - direction[0], y - direction[1]))
        return_list.append((x, y))
        return_list.append((x + direction[0], y + direction[1]))

    elif (
        dfs(board, x, y, player, direction, 2, 2) == True
        and (
            board.get_value(x - direction[0], y - direction[1])
            == board.get_value(x, y)
            == player
        )
        and (
            board.get_value(
                x - direction[0] - direction[0], y - direction[1] - direction[1]
            )
            != (PLAYER2 if player == PLAYER1 else PLAYER1)
        )
    ):
        print("testing", direction, x, y)
        if (
            board.get_value(
                x - direction[0] - direction[0], y - direction[1] - direction[1]
            )
            == board.empty_square
        ):
            return_list.append(
                (x - direction[0] - direction[0], y - direction[1] - direction[1])
            )

        return_list.append((x - direction[0], y - direction[1]))
        return_list.append((x, y))
        return_list.append(
            (x + direction[0] + direction[0], y + direction[1] + direction[1])
        )

    elif (
        dfs(board, x, y, player, (-direction[0], -direction[1]), 2, 2) == True
        and (
            board.get_value(x + direction[0], y + direction[1])
            == board.get_value(x, y)
            == player
        )
        and (
            board.get_value(
                x + direction[0] + direction[0], y + direction[1] + direction[1]
            )
            != (PLAYER2 if player == PLAYER1 else PLAYER1)
        )
    ):
        print("testing_two", direction, x, y)
        if (
            board.get_value(
                x + direction[0] + direction[0], y + direction[1] + direction[1]
            )
            == board.empty_square
        ):
            return_list.append(
                (x + direction[0] + direction[0], y + direction[1] + direction[1])
            )
        return_list.append(
            (x - direction[0] - direction[0], y - direction[1] - direction[1])
        )
        return_list.append((x, y))
        return_list.append((x + direction[0], y + direction[1]))
    return return_list


def make_list_to_direction(board: Board, x, y, dir, n, player):
    print("hello world")

    print(x, y)
    for i in range(1, n):
        if board.get_value(x + (dir[0] * i), y + (dir[1] * i)) == player:
            print(x + (dir[0] * i), y + (dir[1] * i))


def check_positions_and_make_list(list, player):
    for i in range(len(list)):
        print(i)


def check_double_three(board: Board, x, y, player):
    direction = None
    three = []
    for dir in DIRECTIONS:
        if (
            dfs(board, x, y, player, dir, 1, 1) == True
            and is_valid_position((x - dir[0], y - dir[1])) == True
            and board.get_value(x - dir[0], y - dir[1])
            != (PLAYER2 if player == PLAYER1 else PLAYER1)
        ):
            make_list_to_direction(board, x, y, dir, 5, player)
            if board.get_value(x - dir[0], y - dir[1]) == player:
                three.append((x - dir[0], y - dir[1]))
            three.append((x, y))
            if board.get_value(x + dir[0], y + dir[1]) == player:
                three.append((x + dir[0], y + dir[1]))
            if board.get_value(x + dir[0] + dir[0], y + dir[1] + dir[1]) == player:
                three.append((x + dir[0] + dir[0], y + dir[1] + dir[1]))
            if (
                board.get_value(
                    x + dir[0] + dir[0] + dir[0], y + dir[1] + dir[1] + dir[1]
                )
                == player
            ):
                three.append(
                    (x + dir[0] + dir[0] + dir[0], y + dir[1] + dir[1] + dir[1])
                )
            direction = dir
            break
    if direction is None:
        print("a")
        for i in range(len(DIRECTIONS) // 2):
            three = check_next_only_range(board, x, y, DIRECTIONS[i], player)
            if three is not None:
                direction = DIRECTIONS[i]
                break
    print("three", three, direction)
    directions_copy = DIRECTIONS.copy()
    if direction is not None:
        print("direction, rev", direction, (-direction[0], -direction[1]))
        directions_copy.remove(direction)
        directions_copy.remove((-direction[0], -direction[1]))
        for one_place in three:
            for dir in directions_copy:
                if (
                    dfs(board, one_place[0], one_place[1], player, dir, 1, 1) == True
                    and is_valid_position(
                        (one_place[0] - dir[0], one_place[1] - dir[1])
                    )
                    == True
                    and board.get_value(one_place[0] - dir[0], one_place[1] - dir[1])
                    == board.empty_square
                ):
                    print()
                    print(one_place[0], one_place[1], dir)
                    print("double tree found!!!!!!!!!!!!")
                    return True
                elif (
                    len(
                        check_next_only_range(
                            board, one_place[0], one_place[1], dir, player
                        )
                    )
                    != 0
                    # is not None
                ):
                    print("double tree found")
                    return True
    else:
        return False
