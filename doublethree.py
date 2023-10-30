from Board import Board
from config import *


def is_valid_position(position):
    # Check if the position (x, y) is within the bounds of the board.
    return 0 <= position[0] < 19 and 0 <= position[1] < 19


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
    return_list = []
    return_list.append((x, y))
    for i in range(1, n):
        if is_valid_position((x + (dir[0] * i), y + (dir[1] * i))):
            if board.get_value(x + (dir[0] * i), y + (dir[1] * i)) == player:
                return_list.append((x + (dir[0] * i), y + (dir[1] * i)))

    return return_list


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
            three = make_list_to_direction(board, x, y, dir, 5, player)

            # if board.get_value(x - dir[0], y - dir[1]) == player:
            #     three.append((x - dir[0], y - dir[1]))
            # three.append((x, y))
            # if board.get_value(x + dir[0], y + dir[1]) == player:
            #     three.append((x + dir[0], y + dir[1]))
            # if board.get_value(x + dir[0] + dir[0], y + dir[1] + dir[1]) == player:
            #     three.append((x + dir[0] + dir[0], y + dir[1] + dir[1]))
            # if (
            #     board.get_value(
            #         x + dir[0] + dir[0] + dir[0], y + dir[1] + dir[1] + dir[1]
            #     )
            #     == player
            # ):
            #     three.append(
            #         (x + dir[0] + dir[0] + dir[0], y + dir[1] + dir[1] + dir[1])
            #     )
            direction = dir
            break
    if direction is None:
        # print("a")
        for i in range(len(DIRECTIONS) // 2):
            three = check_next_only_range(board, x, y, DIRECTIONS[i], player)
            if three is not None:
                direction = DIRECTIONS[i]
                break
    # print("three", three, direction)
    directions_copy = DIRECTIONS.copy()
    if direction is not None:
        # print("direction, rev", direction, (-direction[0], -direction[1]))
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
