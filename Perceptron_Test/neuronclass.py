import numpy as np

from typing import List

class Neuron:
    def __init__(self, weights : np.array([])):
        self.input_weights = weights
        self.result = 0
        self.localgrad = 0
        self.grad_step = 0.5 # Is chosen manually
        self.entries = np.array([])

    def allow_foo(self, num):
        result = 1 / (1 + np.exp(num))
        return result

    def resulting(self, entry: list):
        self.result = self.allow_foo(np.sum(np.dot(np.array(entry), self.input_weights)))
        self.entries = np.array(entry)
        return self.result

    def back_propogation(self, numeration, next_neurones):
        if next_neurones is None: # Means, it is exit layer
            #current_error =
            self.localgrad = np.exp(1) * self.result * (1 - self.result)
            return
        derivative = self.allow_foo(self.result)
        derivative = derivative - (1 - derivative)
        exit_weights = []
        exit_grads = []
        temp = 0 # Temp variable for multi entry neurones
        for neuron in next_neurones:
            exit_weights.append(neuron.input_weights[numeration])
            exit_grads.append(neuron.localgrad)
        for i in range(0, len(exit_grads)):
            temp += exit_grads[i] * exit_weights[i]
        self.localgrad = temp * derivative
        self.weight_correction()

    def weight_correction(self):
        for i in range(0, len(self.input_weights)):
            self.input_weights[i] = self.input_weights[i] - self.grad_step * self.localgrad * self.entries[i]
