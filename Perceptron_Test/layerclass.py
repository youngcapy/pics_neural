from neuronclass import Neuron
import numpy as np
from typing import List

class Layer:
    def __init__(self, entry_neurones: List[Neuron], prevlayer : 'Layer', nextlayer: 'Layer'):
        self.neurones = entry_neurones
        self.next_layer = nextlayer
        self.prev_layer = prevlayer
        self.results = list()
        self.entries = list()
        self.is_exit = False
        self.true_index = -1 # If is exit layer
        self.learning_process = list() # To visualize a learning process

    def forward_calculation(self):
        if len(self.results) != 0:
            self.results = []
        if len(self.entries) == 0:
            self.get_entries()
        for neuro in self.neurones:
            self.results.append(neuro.resulting(self.entries))
        if self.is_exit:
            self.cross_entropy(self.true_index)



    def soft_maxing(self): # Does, if last layer
        if self.next_layer is not None:
            return
        sm_denom = 0
        sm_results = self.results
        for i in range(0, len(self.results)):
            sm_denom += np.exp(self.results[i])

        for i in range(0, len(self.results)):
            sm_results[i] = np.exp(self.results[i]) / sm_denom
        self.learning_process.append([self.true_index, sm_results[self.true_index]])
        return sm_results

    def cross_entropy(self, true_index : int):
        is_element = len(self.neurones) * [0]
        is_element[true_index] = 1
        soft_maxers = self.soft_maxing()
        result = 0
        for i in range(len(self.neurones)):
            result += is_element[i] * np.log(soft_maxers[i])
        result *= -1

    def back_propogation(self):
        for i in range(0, len(self.neurones)):
            if self.is_exit is True:
                self.neurones[i].back_propogation(i, None)
            else:
                self.neurones[i].back_propogation(i, self.next_layer.neurones)

    def set_next_layer(self, next_link: 'Layer'):
        self.next_layer = next_link

    def set_prev_layer(self, prev_link: 'Layer'):
        self.prev_layer = prev_link

    def set_entries(self, entries_list):
        self.entries = entries_list
    def get_entries(self):
        self.entries = self.prev_layer.results