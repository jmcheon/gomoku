import random


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
    # available = []
    best_score = float("-inf")
    best_move = []
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 0:
                map[i][j] = 2
                score = minmax(map)
                map[i][j] = 0
                if score > best_score:
                    best_score = score
                    best_move = [i, j]

    map[best_move[0]][best_move[1]] = 2


def minmax(board):
    return 1
