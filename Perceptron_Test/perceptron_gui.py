import time
from tkinter import *
import os.path
import csv
from perceptronBuilder import PerceptronBuilder
from helper import picture_reader
import ast

class Gui:
    def __init__(self):

        self.mechanism = PerceptronBuilder()
        self.window = Tk()
        self.window.title("Drawing App")
        self.window.geometry("700x600")

        self.canvas = None
        self.selected_color = "black"
        self.brush_size = 20
        self.is_drawing = False
        self.last_x = 0
        self.last_y = 0

        self.menu_init()
        self.canvas_init()

        self.canvas.bind('<Button-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.stop_drawing)

        self.data_buffer = list()

        self.window.mainloop()
    def menu_init(self):
        menu_bar = Menu(self.window)
        brush_menu = Menu(menu_bar, tearoff=0)
        brush_menu.add_command(label="Select Brush Size", command=self.select_brush_size)

        # Create the clear menu
        clear_menu = Menu(menu_bar, tearoff=0)
        clear_menu.add_command(label="Clear Canvas", command=self.clear_canvas)

        # Create the save menu
        save_menu = Menu(menu_bar, tearoff=0)
        save_menu.add_command(label="Test Drawing", command=self.test_image)

        dataset_menu = Menu(menu_bar, tearoff=0)
        dataset_menu.add_command(label="Choose test dataset", command=self.test_dataset)
        dataset_menu.add_command(label="Choose control dataset", command=self.control_dataset)

        # Add the menus to the menu bar
        menu_bar.add_cascade(label="Brush", menu=brush_menu)
        menu_bar.add_cascade(label="Clear", menu=clear_menu)
        menu_bar.add_cascade(label="Dataset", menu=dataset_menu)
        menu_bar.add_cascade(label="Test image", command=self.test_image)

        # Configure the menu bar
        self.window.config(menu=menu_bar)

    def canvas_init(self):
        self.canvas = Canvas(self.window, width=512, height=512, bg="white")
        self.canvas.pack()

    def select_brush_size(self):
        new_window = Toplevel(self.window)
        new_window.title("Select Brush Size")
        new_window.geometry("400x100")

        brush_size_label = Label(new_window, text="Brush Size")
        brush_size_label.pack()

        brush_size_slider = Scale(new_window, from_=1, to=25, orient=HORIZONTAL, command=self.change_brush_size)
        brush_size_slider.set(self.brush_size)
        brush_size_slider.pack()

    def clear_canvas(self):
        self.canvas.delete("all")

    def test_image(self):

        path = os.path.dirname(os.path.realpath(__file__))
        time.sleep(0.1)
        x1 = self.window.winfo_rootx() + self.canvas.winfo_x()
        y1 = self.window.winfo_rooty() + self.canvas.winfo_y()

        self.canvas.update()

        file_name = "tmp.ps"
        self.canvas.postscript(file=file_name, colormode='color')
        pixels = picture_reader(file_name)
        os.remove(file_name)
        self.mechanism.start(pixels)

    def test_dataset(self):
        self.data_puller()
        for row in self.data_buffer:
            self.mechanism.start(row[1], row[0])
        pass

    def control_dataset(self):
        pass

    def change_brush_size(self, value):
        self.brush_size = int(value)

    def start_drawing(self, event):
        self.is_drawing = True
        self.last_x = event.x
        self.last_y = event.y

    def draw(self, event):

        if self.is_drawing:
            x, y = event.x, event.y
            #self.canvas.create_line(self.last_x, self.last_y, x, y, width=self.brush_size, fill=self.selected_color)
            self.canvas.create_rectangle(self.last_x, self.last_y, x, y, width=self.brush_size, fill=self.selected_color)
            self.last_x = x
            self.last_y = y

    def stop_drawing(self, event):
        self.is_drawing = False

    def data_puller(self):
        filename = "annotation.csv"

        with open(filename, 'r', newline='') as csvfile:
            csvwriter = csv.reader(csvfile)
            for row in csvwriter:
                if row[0] != "id":
                    self.data_buffer.append((row[1], ast.literal_eval(row[3])))
