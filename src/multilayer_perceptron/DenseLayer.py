import numpy as np
from utils import heUniform
from activations import sigmoid, softmax, relu


class Layer:
    def __init__(self):
        self.x = None
        self.y = None

    def forward(self, x):
        pass

    def backward(self, output_gradient, alpha):
        pass


class DenseLayer(Layer):
    def __init__(
        self, input_shape, output_shape, activation, weights_initializer="zero"
    ):
        self.shape = (input_shape, output_shape)

        # Initialize weights and bias
        if weights_initializer == "heUniform":
            self.weights = heUniform((output_shape, input_shape))
            self.weights_initializer = "heUniform"
            self.bias = heUniform(output_shape, 1)
        elif weights_initializer == "random":
            self.weights = np.random.randn(output_shape, input_shape)
            self.weights_initializer = "random"
            self.bias = np.random.randn(output_shape, 1)
        elif weights_initializer == "zero":
            self.weights = np.zeros((output_shape, input_shape))
            self.weights_initializer = "zero"
            self.bias = np.zeros((output_shape, 1))

        # Activation function
        if activation == "sigmoid":
            self.activation = sigmoid
        elif activation == "softmax":
            self.activation = softmax
        elif activation == "ReLU":
            self.activation = relu

    def set_weights(self, weights, bias):
        if weights.shape != self.weights.shape:
            raise ValueError("Incompatible shape of weights.")
        self.weights = weights
        self.bias = bias

    def forward(self, input_data):
        self.input_data = input_data
        z = np.dot(self.weights, self.input_data) + self.bias
        self.z = z
        return self.activation(z)

    def backward(self, output_gradient, alpha):
        activation_gradient = self.activation(self.z) * (1 - self.activation(self.z))

        weights_gradient = np.dot(
            output_gradient * activation_gradient, self.input_data.T
        )
        bias_gradient = output_gradient * activation_gradient

        input_gradient = np.dot(self.weights.T, output_gradient * activation_gradient)
        self.weights -= alpha * weights_gradient
        self.bias -= alpha * output_gradient * activation_gradient

        return input_gradient, weights_gradient, bias_gradient
