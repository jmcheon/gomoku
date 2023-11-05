import random


scores = {5: 100000, 4: 10000, 3: 1000, 2: 100, 1: 10, "tie": 0}


# def equals3(a, b, c):
#     return a == b and b == c and a != 0


# TODO: needs to rework outputting winner and score
def get_score(board, target):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != 0:
                player = board[i][j]  # The current player's value (1 or 2)
                # Check for 5 consecutive elements to the right
                if j + 4 < len(board[0]) and all(
                    board[i][j + k] == player for k in range(target)
                ):
                    return target  # Player 'player' wins

                # Check for 5 consecutive elements downward
                if i + 4 < len(board) and all(
                    board[i + k][j] == player for k in range(target)
                ):
                    return target  # Player 'player' wins

                # Check for 5 consecutive elements diagonally (bottom-right)
                if (
                    i + 4 < len(board)
                    and j + 4 < len(board[0])
                    and all(board[i + k][j + k] == player for k in range(target))
                ):
                    return target  # Player 'player' wins

                # Check for 5 consecutive elements diagonally (top-right)
                if (
                    i - 4 >= 0
                    and j + 4 < len(board[0])
                    and all(board[i - k][j + k] == player for k in range(target))
                ):
                    return target  # Player 'player' wins

    return None


def check_winner(board):
    winner = get_score(board, 5)
    open_spots = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                open_spots += 1

    if winner is None and open_spots == 0:
        return "tie"
    else:
        return winner


def check_score(board):
    winner = None

    max_score = None
    for i in range(5, 1, -1):
        score = get_score(board, i)
        if score is not None:
            if max_score is None:
                max_score = score
            elif score > max_score:
                max_score = score

    winner = max_score

    open_spots = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
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
                score = minmax(
                    board.copy(),
                    4,
                    alpha=float("-inf"),
                    beta=float("inf"),
                    isMaximizing=False,
                )
                print("score", score)
                board[i][j] = 0
                if score > best_score:
                    best_score = score
                    best_move = [i, j]
    print("aa", best_move)
    board[best_move[0]][best_move[1]] = 2


def minmax(board, depth, alpha, beta, isMaximizing):
    # if depth == 0 or game over in position
    # return static evaluation of position
    result = check_score(board)
    if result != None:
        print(result)
        print(scores[result] if isMaximizing is False else -1 * scores[result])
        return scores[result] if isMaximizing is False else -1 * scores[result]
    elif result == "tie":
        return scores["tie"]
    elif depth == 0:
        return 0

    if isMaximizing:
        best_score = float("-inf")
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    board[i][j] = 2
                    score = minmax(board, depth - 1, alpha, beta, False)
                    board[i][j] = 0
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score

    else:
        best_score = float("inf")
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    board[i][j] = 1
                    score = minmax(board, depth - 1, alpha, beta, True)
                    board[i][j] = 0
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score
