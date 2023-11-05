import random


scores = {1: -10, 2: 10, "tie": 0}


def equals3(a, b, c):
    return a == b and b == c and a != 0


def check_winner(board):
    winner = None

    # Horizontal
    for i in range(3):
        if equals3(board[i][0], board[i][1], board[i][2]):
            winner = board[i][0]

    # Vertical
    for i in range(3):
        if equals3(board[0][i], board[1][i], board[2][i]):
            winner = board[0][i]

    # Diagonal
    if equals3(board[0][0], board[1][1], board[2][2]):
        winner = board[0][0]
    if equals3(board[2][0], board[1][1], board[0][2]):
        winner = board[2][0]

    open_spots = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                open_spots += 1

    if winner is None and open_spots == 0:
        return "tie"
    else:
        return winner


def nextTurn(board):
    print(board)
    available = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                available.append((i, j))
    move = random.choice(available)
    print(move)
    board[move[0]][move[1]] = 2


def best_move(board):
    # available = []
    best_score = float("-inf")
    best_move = []
    print(len(board), len(board[0]))
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                board[i][j] = 2
                score = minmax(board.copy(), 0, False)
                print("score", score)
                board[i][j] = 0
                if score > best_score:
                    best_score = score
                    best_move = [i, j]
    print("aa", best_move)
    board[best_move[0]][best_move[1]] = 2


def minmax(board, depth, isMaximizing):
    result = check_winner(board)
    if result != None:
        return scores[result]

    if isMaximizing:
        best_score = float("-inf")
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    board[i][j] = 2
                    score = minmax(board, depth + 1, False)
                    board[i][j] = 0
                    best_score = max(score, best_score)
        return best_score

    else:
        bestScore = float("inf")
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    board[i][j] = 1
                    score = minmax(board, depth + 1, True)
                    board[i][j] = 0
                    bestScore = min(score, bestScore)

        return bestScore
