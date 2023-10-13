import random


scores = {1: -10, 2: 10, None: 0}


def check_winner(board):
    # Check rows
    for row in board:
        if all(cell == 1 for cell in row):
            return 1
        elif all(cell == 2 for cell in row):
            return 2

    # Check columns
    for col in range(3):
        if all(board[row][col] == 1 for row in range(3)):
            return 1
        elif all(board[row][col] == 2 for row in range(3)):
            return 2

    # Check diagonals
    if all(board[i][i] == 1 for i in range(3)) or all(
        board[i][2 - i] == 1 for i in range(3)
    ):
        return 1
    elif all(board[i][i] == 2 for i in range(3)) or all(
        board[i][2 - i] == 2 for i in range(3)
    ):
        return 2
    return None


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
    print(board)
    print(board[0][0], board[1][0])
    # available = []
    best_score = float("-inf")
    best_move = []
    print(len(board), len(board[0]))
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                board[i][j] = 2
                score = minmax(board, 0, False)
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
                    score = minmax(board.copy(), depth + 1, False)
                    board[i][j] = 0
                    best_score = max(score, best_score)
        return best_score

    else:
        bestScore = float("inf")
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    board[i][j] = 1
                    score = minmax(board.copy(), depth + 1, True)
                    board[i][j] = 0
                    bestScore = min(score, bestScore)

        return bestScore
