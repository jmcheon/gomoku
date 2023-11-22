import math
import random


class TreeNode:
    def __init__(self, board, parent, prior_probs=0.0):
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
        # the action value of the node
        self.action_value = 0
        self.prior_probs = prior_probs
        # current node's children
        self.children = {}


class MCTS:
    def __init__(self, model):
        self.model = model
        self.game_state = [np.zeros((19, 19)) for _ in range(17)]

    # search for the best move in the current position
    def search(self, initial_state):
        # create root node
        self.root = TreeNode(initial_state, None)

        for iteration in range(300):
            # select a node (selection phase)
            node = self.select(self.root)

            move_probs, vlaue = self.evaluate_board(node.board)

            # backpropagate results
            self.backpropagate(node, value)

       # pick up the best move in the current position
       return self.select_action(self.root)

    # select most promising node
    def select(self, node):
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = node.children[self.select_action(node)]
            else:
                return self.expand(node)
        return node

    # expand node
    def expand(self, node):
        # generate legal states for the given node
        state_lst = node.board.generate_states()
        for board, action in state_lst:
            # print("state:", state)
            # make sure the current state is not present in child nodes
            if str(board.position) not in node.children:
                # Get the prior probability for this state from the policy head of the neural network.
                self.preprocess_board(board, board.turn)
                policy_probs, _ = self.model.predict(self.game_state)
                action_index = self.action_to_index(action)
                prior_prob = policy_probs[action_index]

                # create a new node
                new_node = TreeNode(state, node, prior_prob)

                # add child node to parent's node children list (dict)
                node.children[action] = new_node

                # case when node is fully expanded
                if len(state_lst) == len(node.children):
                    node.is_fully_expanded = True

                # return newly created node
                return new_node

    def evaluate_board(self, board):
        self.preprocess_board(board)

        # predict the move probabilities(p) and the value(v) of the board state.
        move_probs, value = self.model.predict(self.game_state)

        return move_probs, value

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

    def backpropagate(self, search_path, value, to_play):
        """Backpropagate the value through the nodes in the search path"""
        for node in reversed(search_path):
            node.visits += 1
            # Note: The value is from the perspective of the current player,
            # so we need to invert it when the player to play is not the current player
            node.total_value += value if node.to_play == to_play else -value

    # backpropagate the number of visits and action_value up to the root node
    def backpropagate(self, node, action_value):
        # update nodes's up to root node
        while node is not None:
            # update node's visits
            node.visits += 1

            # update node's action_value
            node.action_value += action_value

            # set node to parent
            node = node.parent

    def select_action(self, node):
        best_score = float("-inf")
        best_action = None

        for action, child_node in node.children.items():
            Q = child_node.total_value / child_node.visits  # average value
            U = child_node.prior_prob / (1 + child_node.visits)  # exploration term
            score = Q + U

            if score > best_score:
                best_score = score
                best_action = action

        return best_action

    def action_to_index(self, action):
        # Convert an action to an index into the policy_probs array.
        # Since your action is likely a 2D tuple (row, col) and policy_probs is a 1D array,
        # you need to flatten the action to get the correct index.
        return np.ravel_multi_index(action, (NUM_LINES, NUM_LINES))
