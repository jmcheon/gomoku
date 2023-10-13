import random


scores = {1: -10, 2: 10, None: 0}


def check_winner(map):
    # Check rows
    for row in map:
        if all(cell == 1 for cell in row):
            return 1
        elif all(cell == 2 for cell in row):
            return 2

    # Check columns
    for col in range(3):
        if all(map[row][col] == 1 for row in range(3)):
            return 1
        elif all(map[row][col] == 2 for row in range(3)):
            return 2

    # Check diagonals
    if all(map[i][i] == 1 for i in range(3)) or all(
        map[i][2 - i] == 1 for i in range(3)
    ):
        return 1
    elif all(map[i][i] == 2 for i in range(3)) or all(
        map[i][2 - i] == 2 for i in range(3)
    ):
        return 2
    return None


def nextTurn(map):
    print(map)
    available = []
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 0:
                available.append((i, j))
    move = random.choice(available)
    print(move)
    map[move[0]][move[1]] = 2


def best_move(map):
    print(map)
    print(map[0][0], map[1][0])
    # available = []
    best_score = float("-inf")
    best_move = []
    print(len(map), len(map[0]))
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 0:
                map[i][j] = 2
                score = minmax(map, 0, False)
                print("score", score)
                map[i][j] = 0
                if score > best_score:
                    best_score = score
                    best_move = [i, j]
    print("aa", best_move)
    map[best_move[0]][best_move[1]] = 2


def minmax(map, depth, isMaximizing):
    result = check_winner(map)
    if result != None:
        score = scores[result]
        # print("result:", score)
        return score

    if isMaximizing:
        best_score = float("-inf")
        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j] == 0:
                    map[i][j] = 2
                    score = minmax(map, depth + 1, False)
                    map[i][j] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j] == 0:
                    map[i][j] = 1
                    score = minmax(map, depth + 1, True)
                    map[i][j] = 0
                    best_score = min(score, best_score)

        return best_score
