from src.game.board import Board
from config import *


def is_valid_position(position):
    # Check if the position (x, y) is within the bounds of the board.
    return 0 <= position[0] < NUM_LINES and 0 <= position[1] < NUM_LINES


def make_list_to_direction(board: Board, x, y, dir, n, player):
    return_list = []
    return_list.append((x, y))
    for i in range(1, n):
        if is_valid_position((x + (dir[0] * i), y + (dir[1] * i))):
            if board.get_value(x + (dir[0] * i), y + (dir[1] * i)) == player:
                return_list.append((x + (dir[0] * i), y + (dir[1] * i)))

    return return_list


def dfs(board: Board, x, y, player, direction, count, player_count):
    if count > 4:
        return False
    nx = x + direction[0]
    if nx > NUM_LINES:
        return False
    ny = y + direction[1]
    if ny > NUM_LINES:
        return False

    if 3 <= count and count <= 4:
        if (
            player_count >= 3
            and is_valid_position((nx, ny)) == True
            and board.get_value(nx, ny)
            != (PLAYER_2 if player == PLAYER_1 else PLAYER_1)
        ):
            return True
        # else:
        #     return False

    if not is_valid_position((nx, ny)):
        return False

    if board.get_value(nx, ny) == (PLAYER_2 if player == PLAYER_1 else PLAYER_1):
        return False

    if board.get_value(nx, ny) == player:
        player_count += 1

    return dfs(board, nx, ny, player, direction, count + 1, player_count)


def check_next_only_range(board: Board, x, y, dir, player):
    return_list = []
    print("direction", dir, (-dir[0], -dir[1]), player)
    if (
        is_valid_position((x + dir[0], y + dir[1])) is False
        or is_valid_position((x + dir[0] + dir[0], y + dir[1] + dir[1])) is False
        or is_valid_position((x - dir[0], y - dir[1])) is False
        or is_valid_position((x - dir[0] - dir[0], y - dir[1] - dir[1])) is False
    ):
        return None
    if (
        board.get_value(x + dir[0], y + dir[1])
        == board.get_value(x - dir[0], y - dir[1])
        == player
    ):
        # print("hello world")
        return_list = make_list_to_direction(board, x, y, (-dir[0], -dir[1]), 3, player)
        return_list += make_list_to_direction(board, x, y, dir, 3, player)
        if board.get_value(x + (dir[0] * 2), y + (dir[1] * 2)) != (
            PLAYER_2 if player == PLAYER_1 else PLAYER_1
        ) and board.get_value(x - (dir[0] * 2), y - (dir[1] * 2)) != (
            PLAYER_2 if player == PLAYER_1 else PLAYER_1
        ):
            print("word")
        # if board.get_value(x - dir[0] - dir[0], y - dir[1] - dir[1]) == player:
        #     return_list.append((x - dir[0] - dir[0], y - dir[1] - dir[1]))
        # return_list.append((x - dir[0], y - dir[1]))
        # return_list.append((x, y))
        # return_list.append((x + dir[0], y + dir[1]))
        # if board.get_value(x + dir[0] + dir[0], y + dir[1] + dir[1]) == player:
        #     return_list.append(x + dir[0] + dir[0], y + dir[1] + dir[1])

    elif (
        dfs(board, x, y, player, dir, 2, 2) == True
        and (board.get_value(x - dir[0], y - dir[1]) == board.get_value(x, y) == player)
        and (
            board.get_value(x - dir[0] - dir[0], y - dir[1] - dir[1])
            != (PLAYER_2 if player == PLAYER_1 else PLAYER_1)
        )
    ):
        # TODO: 3 for dfs, 2 for opposite
        print("testing", dir, x, y)
        return_list = make_list_to_direction(board, x, y, (-dir[0], -dir[1]), 3, player)
        return_list += make_list_to_direction(board, x, y, dir, 3, player)
        # if (
        #     board.get_value(x - dir[0] - dir[0], y - dir[1] - dir[1])
        #     == board.empty_square
        # ):
        #     return_list.append((x - dir[0] - dir[0], y - dir[1] - dir[1]))

        # return_list.append((x - dir[0], y - dir[1]))
        # return_list.append((x, y))
        # return_list.append((x + dir[0] + dir[0], y + dir[1] + dir[1]))

    elif (
        dfs(board, x, y, player, (-dir[0], -dir[1]), 2, 2) == True
        and (board.get_value(x + dir[0], y + dir[1]) == board.get_value(x, y) == player)
        and (
            board.get_value(x + dir[0] + dir[0], y + dir[1] + dir[1])
            != (PLAYER_2 if player == PLAYER_1 else PLAYER_1)
        )
    ):
        return_list = make_list_to_direction(board, x, y, dir, 3, player)
        return_list += make_list_to_direction(
            board, x, y, (-dir[0], -dir[1]), 3, player
        )
        # TODO: 3 for dfs(opposite), 2 for reg.
        # print("testing_two", dir, x, y)
        # if (
        #     board.get_value(x + dir[0] + dir[0], y + dir[1] + dir[1])
        #     == board.empty_square
        # ):
        #     return_list.append((x + dir[0] + dir[0], y + dir[1] + dir[1]))
        # return_list.append((x - dir[0] - dir[0], y - dir[1] - dir[1]))
        # return_list.append((x, y))
        # return_list.append((x + dir[0], y + dir[1]))
        return_list = make_list_to_direction(board, x, y, (-dir[0], -dir[1]), 3, player)
        return_list += make_list_to_direction(board, x, y, dir, 3, player)
    print(return_list)
    return_list = list(set(return_list))
    return return_list


def check_double_three(board: Board, x, y, player):
    direction = None
    cont_range = []
    for dir in DIRECTIONS:
        if (
            dfs(board, x, y, player, dir, 1, 1) == True
            and is_valid_position((x - dir[0], y - dir[1])) == True
            and board.get_value(x - dir[0], y - dir[1])
            != (PLAYER_2 if player == PLAYER_1 else PLAYER_1)
        ):
            cont_range = make_list_to_direction(board, x, y, dir, 5, player)

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
        print("a")
        for i in range(len(DIRECTIONS) // 2):
            cont_range = check_next_only_range(board, x, y, DIRECTIONS[i], player)
            # print("cont_range", cont_range)
            if cont_range:
                direction = DIRECTIONS[i]
                break
    # print("three", three, direction)
    directions_copy = DIRECTIONS.copy()
    if direction is not None:
        # print("direction, rev", direction, (-direction[0], -direction[1]))
        directions_copy.remove(direction)
        directions_copy.remove((-direction[0], -direction[1]))
        for one_place in cont_range:
            for dir in directions_copy:
                if (
                    dfs(board, one_place[0], one_place[1], player, dir, 1, 1) == True
                    and is_valid_position(
                        (one_place[0] - dir[0], one_place[1] - dir[1])
                    )
                    == True
                    and board.get_value(one_place[0] - dir[0], one_place[1] - dir[1])
                    == EMPTY_SQUARE
                ):
                    print()
                    print(one_place[0], one_place[1], dir)
                    print("double tree found!!!!!!!!!!!!")
                    return True
                elif (
                    check_next_only_range(
                        board, one_place[0], one_place[1], dir, player
                    )
                    != None
                    and len(
                        check_next_only_range(
                            board, one_place[0], one_place[1], dir, player
                        )
                    )
                    != 0
                    # is not None
                ):
                    print("double tree found")
                    return True
    return False
