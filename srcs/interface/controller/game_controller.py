import pickle
from datetime import datetime

import pygame
from config import *
from srcs.algo.mcts import MCTS
from srcs.interface.model.game_model import GameModel
from srcs.interface.view.game_view import GameView

# from srcs.interface.game_interface import GameInterface


class GameController:
    def __init__(self, width, height, model):
        pygame.init()
        self.model = model
        self.width = width
        self.height = height
        self.view = None
        self.game_model = None
        self.mode = None
        self.mcts = MCTS(model)
        self.running = True
        self.winner = None
        self.is_ternimal = False

    def init_game(self):
        self.view = GameView(self.width, self.height)
        # TODO: load option configuration values and pass to self.game_logic
        game_option = self.view.new()
        self.view._initialize_game_view()
        self.game_model = GameModel()
        self.game_model.set_config(game_option)
        if game_option != "selfplay":
            self.mode = game_option["mode"]
        self.view.screen.fill(WHITE)
        # self.view.set_game_model(self.game_model)

    def init_selfplay(self):
        self.view = GameView(self.width, self.height)
        # game_option = self.interface.new()
        self.view._initialize_game_view()
        self.game_model = GameModel()
        self.game_model.set_config("selfplay")
        self.mode = "selfplay"
        self.view.screen.fill(WHITE)

    def run(self):
        while self.running:
            if self.view.modal_window.is_open:
                if self.view.modal_window.wait_for_response() == RESET:
                    self.view.reset_requested = True
            else:
                self.view.update_board_and_player_turn(
                    self.game_model.board, self.game_model.record
                )
                if self.mode == "single":
                    self.events_single()
                elif self.mode == "selfplay":
                    self.events_selfplay()
                # else:
                #     self.events_selfplay()
            # Check for a reset condition (e.g., a key press 'R')
            self.view.draw(self.mode)
            if self.view.reset_requested:
                self.view.reset_requested = False  # Reset the flag
                if self.mode == "selfplay":
                    self.init_selfplay()
                else:
                    self.init_game()  # Go back to the main menu

    def get_reward(self):
        if self.winner == None:
            return 0
        elif self.winner == self.game_model.board.turn:
            return 1
        else:
            return -1

    def add_reward_in_game_data(self):
        game_data_with_rewards = []
        print(f"winner: {self.winner}, turn: {self.game_model.board.turn}")
        print(f"game_data: {self.game_model.game_data}")
        for board, action in self.game_model.game_data:
            reward = self.get_reward()
            game_data_with_rewards.append((board, action, reward))
            self.game_model.game_data = game_data_with_rewards
        print(self.game_model.game_data)

    def save_model(self, model_name):
        """
        Args:
            model_name: in the format .h5
        """
        model.save(f"{model_name}.h5")

    def load_model(self, model_name):
        model = load_model(model_name)

    def get_game_data_file_name(self):
        now = datetime.now()

        # convert it to a string in the format 'YYYYMMDD_HHMMSS'
        timestamp_str = now.strftime("%Y%m%d_%H%M%S")

        file_name = f"game_data_{timestamp_str}.pkl"

        return file_name

    def save_game_data(self, file_name):
        with open(file_name, "wb") as f:
            pickle.dump(self.game_model.game_data, f)

    def load_game_data(self, file_name):
        with open(file_name, "rb") as f:
            pickle.dump(self.game_model.game_data, f)

    def play_ai(self):
        print("board before mcts:\n", self.game_model.board)
        _, action = self.mcts.search(self.game_model.board)

        grid_x, grid_y = action
        print(f"selected action: {action}")
        self.game_model.place_stone(grid_x, grid_y)

        self.check_terminate_state()
        self.game_model.change_player_turn()
        self.view.update_board_and_player_turn(
            self.game_model.board, self.game_model.record
        )

    def is_already_occupied(self, grid_x, grid_y):
        if not self.game_model.board.is_empty_square(grid_x, grid_y):
            # TODO: change log message
            self.view.text_box.append_html_text("this cell is already occupied<br>")
            return True
        return False

    def is_capturing_stone(self, grid_x, grid_y):
        capture_list = self.game_model.capture_opponent(grid_x, grid_y)
        if capture_list:
            self.game_model.place_stone(grid_x, grid_y, captured_list=capture_list)
            self.view.text_box.append_html_text("capture gogo <br>")
            return True
        return False

    def check_terminate_state(self):
        if self.game_model.board.is_win_board():
            self.winner = self.game_model.board.turn
            self.is_terminal = True
            self.add_reward_in_game_data()
            self.view.modal_window.set_modal_message(
                f"Game Over! Player {1 if self.game_model.board.turn == PLAYER_1 else 2} Wins!"
            )
            self.view.modal_window.open_modal()
            # TODO: change log message
            self.view.text_box.append_html_text("Game Over. <br>")
        elif self.game_model.is_draw():
            self.is_terminal = True
            self.add_reward_in_game_data()
            self.view.modal_window.set_modal_message(f"Game is drawn.")
            # TODO: change log message
            self.view.text_box.append_html_text("Game is drawn.<br>")

    def convert_pos_to_coordinates(self, x, y):
        return (x + 1, chr(ord("A") + y))

    def events_single(self):
        if self.game_model.board.turn == PLAYER_2:
            self.play_ai()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.view.reset_requested:
                if event.button == 1:
                    # need this
                    grid_x, grid_y = self.view._convert_mouse_to_grid()
                    if self.is_already_occupied(grid_x, grid_y) == True:
                        break
                    if self.is_capturing_stone(grid_x, grid_y) is False:
                        if self.game_model.check_doublethree(grid_x, grid_y) is False:
                            self.game_model.place_stone(grid_x, grid_y)
                            self.view.text_box.append_html_text(
                                f"Stone placed on {self.convert_pos_to_coordinates(grid_x,grid_y)[0]}{self.convert_pos_to_coordinates(grid_x,grid_y)[1]}<br>"
                            )
                            self.check_terminate_state()
                            self.game_model.change_player_turn()
                            self.view.update_board_and_player_turn(
                                self.game_model.board, self.game_model.record
                            )
                        else:
                            # TODO: change log message related
                            self.view.text_box.append_html_text(
                                f"doublethree detected{123} <br>"
                            )
                    self.view.text_box.update(5.0)
                elif event.button == 3:
                    if self.game_model.undo_last_move() is False:
                        self.view.text_box.append_html_text(
                            "Trace is empty, cannot go back further<br>"
                        )
            self.view.ui_manager.process_events(event)

    def events_selfplay(self):
        self.play_ai()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     pass
            self.view.ui_manager.process_events(event)

    # def run_debug(self):
    #     while self.view.running:
    #         self.view.run_debug()
