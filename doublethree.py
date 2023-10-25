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
        if player_count == 3 and board.get_value(nx, ny) == board.empty_square:
            return True

    if not is_valid_position((nx, ny)):
        return False

    if board.get_value(nx, ny) == (PLAYER2 if player == PLAYER1 else PLAYER2):
        return False

    if board.get_value(nx, ny) == player:
        player_count += 1

    return dfs(board, nx, ny, player, direction, count + 1, player_count)


def find_all_continuous(board: Board, x, y, player, direction):
    print("player", player, direction)
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
        or is_valid_position((x - direction[0], y - direction[1])) is False
    ):
        return False
    if (
        board.get_value(x, y)
        == board.get_value(x + direction[0], y + direction[1])
        == board.get_value(x - direction[0], y - direction[1])
        == player
    ):
        return True
    elif dfs(board, x, y, player, direction, 2, 2) == True and (
        board.get_value(x - direction[0], y - direction[1])
        == board.get_value(x, y)
        == player
    ):
        return True
    elif dfs(board, x, y, player, (-direction[0], -direction[1]), 2, 2) == True and (
        board.get_value(x + direction[0], y + direction[1])
        == board.get_value(x, y)
        == player
    ):
        return True
    return False


def check_double_three(board: Board, x, y, player):
    print("init", x, y)
    directions = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
    direction = None
    for dir in directions:
        if dfs(board, x, y, player, dir, 1, 1) == True:
            # three_count +=1
            direction = dir
            break
    # print("first_none", direction)
    if direction is None:
        for i in range(len(directions) // 2):
            if check_next_only_range(board, x, y, directions[i], player) is True:
                direction = directions[i]
                break
    # print("direction", direction)
    if direction is not None:
        print("direction, rev", direction, (-direction[0], -direction[1]))
        directions.remove(direction)
        directions.remove((-direction[0], -direction[1]))
        # print("directions", directions)
        all_cont = find_all_continuous(board, x, y, player, direction)
        print("all_cont", all_cont)
        for one_place in all_cont:
            # print("one_place:", one_place)
            print("=============")
            for dir in directions:
                print("directions", dir)
                if dfs(board, one_place[0], one_place[1], player, dir, 1, 1) == True:
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
            print("=============")

        ## remove direction from 'directions' and do the dfs again
    else:
        return False

    # print("three_count", three_count)
    # if three_count >= 2:
    #     print("Double Three Found!")
    #     return True
    # else:
    #     print("Double Three Not Found")
    #     return False


def inversely_proportional_coordinates(x, y, board_size=19):
    coordinates = []

    # Generate coordinates in one direction (x increasing, y decreasing)
    while x < board_size and y >= 0:
        coordinates.append((x, y))
        x += 1
        y -= 1

    # Reset the coordinates and generate in the other direction (x decreasing, y increasing)
    x, y = x - 1, y + 1
    while x >= 0 and y < board_size:
        coordinates.append((x, y))
        x -= 1
        y += 1

    return coordinates


if __name__ == "__main__":
    x, y = 10, 1  # Replace with your desired coordinates
    for i in range(min(x, y), 0, -1):
        print(x - i, y - i)
    # inversely_proportional_coords = inversely_proportional_coordinates(x, y)
    for i in range(1, min(NUM_LINES - x, NUM_LINES - y)):
        print(x + i, y + i)
    # print(inversely_proportional_coords)
