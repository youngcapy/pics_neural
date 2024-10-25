import collections
import numpy as np

import os
import json
from random import random
from typing import List
from layerclass import Layer
from pathlib import Path
import helper
from neuronclass import Neuron
from helper import weight_gen, layer_builder
from typing import List, Optional


class PerceptronBuilder:

    def __init__(self):
        self.epoch_quantity = 32 # Default wanted epoch quantity
        self.exit_neurons = 10 # Default value for 10 classes
        self.wanted_hid_layer_quantity = 0 # Default value (does not contain first after enterlayer)
        self.hidden_layer_neurons = 689 # Default value for 1-layer MLP
        self.enters = 1024 # for 32x32 picture
        self.layers : List[Layer] = []
        self.data_buffer = []
        self.mlp_init()

    def mlp_init(self):

        with open('perceptron_conf.json', 'r+') as conf: # Loads MLP configuration
            data = json.load(conf)
            if len(data) != 0:
                print(0)

        self.layers.append(layer_builder(self.hidden_layer_neurons, self.enters, None, None))
        for i in range(0, self.wanted_hid_layer_quantity):
            self.layers.append(layer_builder(self.hidden_layer_neurons, self.hidden_layer_neurons**2, None, None))
            if i > 1:
                self.layers[i - 1].set_next_layer(self.layers[i])
                self.layers[i].set_prev_layer(self.layers[i - 1])
        self.layers.append(layer_builder(self.exit_neurons, self.hidden_layer_neurons, self.layers[len(self.layers) - 1], None))

        self.layers[len(self.layers) - 2].set_next_layer(self.layers[len(self.layers) - 1])
        self.layers[len(self.layers) - 1].is_exit = True
    def start(self, entry, *args):
        results_dict = \
            {"A_Letters": 0,
             "G_Letters": 1,
             "J_Letters": 2,
             "K_Letters": 3,
             "L_Letters": 4,
             "P_Letters": 5,
             "Q_Letters": 6,
             "R_Letters": 7,
             "W_Letters": 8,
             "Z_Letters": 9,
             }
        if len(args) > 0:
            expected_res = results_dict[args[0]]
            hot_encoded = [0] * len(results_dict)
            hot_encoded[expected_res] = 1
            self.layers[len(self.layers) - 1].true_index = expected_res
        entry = np.array(entry).ravel().tolist()
        self.layers[0].set_entries(entry)
        for i in range(0, len(self.layers)):
            self.layers[i].forward_calculation()
        for i in range(len(self.layers) - 1, -1, -1):
            self.layers[i].back_propogation()
        pass