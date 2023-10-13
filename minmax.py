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
