from etc.Gomoku import Gomoku
from config import *
import sys
import os

path = os.path.join(os.path.dirname(__file__), "..", MLP_DIR_NAME)
sys.path.insert(1, path)
# from DenseLayer import DenseLayer
# from NeuralNet import NeuralNet


# def create_model():
#     model = NeuralNet()
#     model.create_network(
#         [
#             DenseLayer(INPUT_SHAPE, 200, activation="ReLU"),
#             DenseLayer(200, 100, activation="ReLU", weights_initializer="zero"),
#             DenseLayer(100, 50, activation="ReLU", weights_initializer="zero"),
#             DenseLayer(
#                 50, OUTPUT_SHAPE, activation="softmax", weights_initializer="zero"
#             ),
#         ]
#     )
#     return model


if __name__ == "__main__":
    # model = create_model()
    gomoku = Gomoku()
    gomoku.play()
