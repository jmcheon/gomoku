import math
import random


class TreeNode:
    def __init__(self, board, parent):
        self.board = board
        # init is node terminal flag
        if board.is_win() or board.is_draw():
            self.is_terminal = True
        else:
            self.is_terminal = False

        # init is fully expanded flag
        self.is_fully_expanded = self.is_terminal
        self.parent = parent
        # the number of node visitis
        self.visits = 0
        # the total score of the node
        self.score = 0
        # current node's children
        self.children = {}


class MCTS:
    def __init__(self, model):
        self.model = model
        self.game_state = np.zeros((19, 19, 17))
        self.game_state = [np.zeros((19, 19)) for _ in range(17)]

    # search for the best move in the current position
    def search(self, initial_state):
        # create root node
        self.root = TreeNode(initial_state, None)

        for iteration in range(300):
            # select a node (selection phase)
            node = self.select(self.root)

            # score current node (simulation phase)
            score = self.rollout(node.board)

            # backpropagate results
            self.backpropagate(node, score)

        # pick up the best move in the current position
        try:
            return self.get_best_move(self.root, 0)  # exploration rate
        except:
            pass

    # select most promising node
    def select(self, node):
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.get_best_move(node, 2)
            else:
                return self.expand(node)
        return node

    # expand node
    def expand(self, node):
        # generate legal states for the given node
        state_lst = node.board.generate_states()
        for state in state_lst:
            # print("state:", state)
            # make sure the current state is not present in child nodes
            if str(state.position) not in node.children:
                # create a new node
                new_node = TreeNode(state, node)

                # add child node to parent's node children list (dict)
                node.children[str(state.position)] = new_node

                # case when node is fully expanded
                if len(state_lst) == len(node.children):
                    node.is_fully_expanded = True

                # return newly created node
                return new_node

    # simulate the game via making random moves until reach end of the game
    def rollout2(self, board):
        # make random moves for both sides until terminal state of the game is reached
        while not board.is_win():
            # try to make a move
            try:
                # make the on board
                board = random.choice(board.generate_states())
                # print(board)
                # input()

            # no moves available
            except:
                # print(board)
                # return a draw score
                return 0
        # print(board)

        # return score from the player "x" perspective
        if board.player2 == PLAYER_1:
            return 1
        elif board.player2 == PLAYER_2:
            return -1

    def rollout(self, board):
        self.preprocess_board(board)

        # predict the move probabilities(p) and the value(v) of the board state.
        move_probs, value = self.model.predict(self.game_state)
        print(f"move_probs(p): {move_probs}, value(v): {value}")

        # TODO: select a move based on the move probabilites and apply it to the board
        """
        # use the move probabilities to select the next move.
        next_move = self.select_move(move_probs)

        # apply the selected move to get the new board state.
        new_board = board.apply_move(next_move)

        # return the predicted value of the new board state.
        return value
        """

    def preprocess_board(self, board, player_turn) -> None:
        """
        Convert the board state to a suitable format for the model.

            self.game_state = [X_t, Y_t, X_t-1, Y_t-1, ... X_t-7, Y_t-7, C]
            X: 8 feature planes of black stone
            Y: 8 feature planes of white stone
            C: the color of player stone; 1 for black, 0 for white
        """
        # get each board state of black and white from the current board position
        player_1_state = board.create_board_state(PLAYER_1)
        player_2_state = board.create_board_state(PLAYER_2)

        # insert each board state of black and white to the beginning of the game_state list
        self.game_state.insert(0, player_1_state)
        self.game_state.insert(1, player_2_state)

        # remove the second and third board states to the last
        del self.game_state[-3:-1]

        # last element of the game_state standing for the color of the player stone; 1 for black, 0 for white
        if player_turn == PLAYER_1:
            self.game_state[-1] = np.zeros((19, 19))
        else:
            self.game_state[-1] = np.ones((19, 19))

    def select_move(self, move_probs):
        next_move = np.argmax(move_probs)
        return next_move

    # backpropagate the number of visits and score up to the root node
    def backpropagate(self, node, score):
        # update nodes's up to root node
        while node is not None:
            # update node's visits
            node.visits += 1

            # update node's score
            node.score += score

            # set node to parent
            node = node.parent

    # select the best node basing on UCB1 formula
    def get_best_move(self, node, exploration_constant):
        best_score = float("-inf")
        best_moves = []

        for child_node in node.children.values():
            # define current player
            if child_node.board.player2 == "X":
                current_player = 1
            if child_node.board.player2 == "O":
                current_player = -1

            # get move score using UCT formula
            move_score = (
                current_player * child_node.score / child_node.visits
                + exploration_constant
                * math.sqrt(math.log(node.visits / child_node.visits))
            )
            # print(move_score)

            # better move has been found
            if move_score > best_score:
                best_score = move_score
                best_moves = [child_node]
            # found as good move as already available
            elif move_score == best_score:
                best_moves.append(child_node)

        # return one of the best moves randomly
        # best_move = random.choice(best_moves)
        # print("best_move board:", best_move.board)
        print(f"best_moves: {best_moves}")
        return random.choice(best_moves)
