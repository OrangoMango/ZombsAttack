from tkinter import *

class Statistics:
        def __init__(self, game):
                self.game = game
                self.frame = LabelFrame(game.tk, text="Your stat", width=100, height=200)
                self.frame.grid(column=1, row=1)
                self.data = {"Kills":0}
                self.labels = []

                self.show_data()
        def show_data(self):
                for k, v in self.data.items():
                        l = Label(self.frame, text="{0}: {1}".format(k, v))
                        l.pack()
                        self.labels.append(l)
