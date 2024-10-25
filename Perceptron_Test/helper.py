from random import random
from PIL import Image
from layerclass import Layer
import os
from neuronclass import Neuron

def weight_gen():
    return 2 * random() - 1  # Generating random weight from -1 to 1

def layer_builder(neurons_quantity: int, prev_neurons_quantity: int, prev_layer: Layer, next_layer: Layer):
    neurons = []
    for i in range(0, neurons_quantity):
        weights = []
        for j in range(0, prev_neurons_quantity):
            weights.append(weight_gen())  # Generating random weight from -1 to 1
        neurons.append(Neuron(weights))
    result = Layer(neurons, prev_layer, next_layer)
    return result

def picture_reader(path):

    ps_image = Image.open(path)
    new_path = 'pic.bmp'
    ps_image.save(new_path)

    with Image.open(new_path) as im:
        resized = im.resize((32, 32)).convert("RGB")
        width, height = resized.size
        pixel_array = []

        for y in range(height):
            row = []
            for x in range(width):
                r, g, b = resized.getpixel((x, y))

                if (r, g, b) == (255, 255, 255): # Some error
                    row.append(0)
                else:
                    row.append(1)

            pixel_array.append(row)
        os.remove(new_path)

        return pixel_array