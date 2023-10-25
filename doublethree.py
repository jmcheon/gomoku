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
    nx = x + direction[0]
    ny = y + direction[1]

    if 3 <= count and count <= 4:
        if (
            player_count == 3
            and is_valid_position((nx, ny)) == True
            and board.get_value(nx, ny) == board.empty_square
        ):
            return True
        else:
            return False

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
    # board
    # print("next_only", x + direction[0], y + direction[1])
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
        return False
    if (
        board.get_value(x, y)
        == board.get_value(x + direction[0], y + direction[1])
        == board.get_value(x - direction[0], y - direction[1])
        == player
    ):
        if (
            board.get_value(
                x + direction[0] + direction[0], y + direction[1] + direction[1]
            )
            == board.empty_square
            and board.get_value(
                x - direction[0] - direction[0], y - direction[1] - direction[1]
            )
            == board.empty_square
        ):
            return True
        else:
            return False
    elif dfs(board, x, y, player, direction, 2, 2) == True and (
        board.get_value(x - direction[0], y - direction[1])
        == board.get_value(x, y)
        == player
    ):
        if (
            board.get_value(
                x - direction[0] - direction[0], y - direction[1] - direction[1]
            )
            == board.empty_square
        ):
            return True
        else:
            return False
    elif dfs(board, x, y, player, (-direction[0], -direction[1]), 2, 2) == True and (
        board.get_value(x + direction[0], y + direction[1])
        == board.get_value(x, y)
        == player
    ):
        if (
            board.get_value(
                x + direction[0] + direction[0], y + direction[1] + direction[1]
            )
            == board.empty_square
        ):
            return True
        else:
            return False
    return False


def check_double_three(board: Board, x, y, player):
    # print("init", x, y, player)
    directions = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
    direction = None
    for dir in directions:
        if (
            dfs(board, x, y, player, dir, 1, 1) == True
            and is_valid_position((x - dir[0], y - dir[1])) == True
            and board.get_value(x - dir[0], y - dir[1]) == board.empty_square
        ):
            direction = dir
            break
    if direction is None:
        for i in range(len(directions) // 2):
            if check_next_only_range(board, x, y, directions[i], player) is True:
                direction = directions[i]
                break
    if direction is not None:
        print("direction, rev", direction, (-direction[0], -direction[1]))
        directions.remove(direction)
        directions.remove((-direction[0], -direction[1]))
        ### TODO
        all_cont = find_all_continuous(board, x, y, player, direction)
        ### TODO
        for one_place in all_cont:
            for dir in directions:
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
                    check_next_only_range(
                        board, one_place[0], one_place[1], dir, player
                    )
                    == True
                ):
                    print("double tree found")
                    return True
    else:
        return False


if __name__ == "__main__":
    # x, y = 10, 1  # Replace with your desired coordinates
    # for i in range(min(x, y), 0, -1):
    #     print(x - i, y - i)
    # # inversely_proportional_coords = inversely_proportional_coordinates(x, y)
    # for i in range(1, min(NUM_LINES - x, NUM_LINES - y)):
    #     print(x + i, y + i)
    # # print(inversely_proportional_coords)

    # direction(1, -1)
    x = 17
    y = 15
    for i in range(min(x, y), 0, -1):
        print((x + i, y - i))
    print("-------------------------")
    for i in range(1, min(NUM_LINES - x, NUM_LINES - y)):
        print((x - i, y + i))
