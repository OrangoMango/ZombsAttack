from tkinter import *

class MiniZombie:
        def __init__(self, minimap, rx, ry):
                self.minimap = minimap
                x, y = int(rx/minimap.frac), int(ry/minimap.frac)
                self.id = self.minimap.canvas.create_oval(x, y, x+50/minimap.frac, y+50/minimap.frac, fill="green")
        def draw(self, x, y):
                self.minimap.canvas.move(self.id, x/self.minimap.frac, y/self.minimap.frac)
        def delete(self):
                self.minimap.canvas.delete(self.id)

class MiniMap:
        def __init__(self, game):
                self.game = game
                self.frac = 7
                self.canvas = Canvas(self.game.tk, width=100, height=100, bg="white")
                self.canvas.grid(column=1, row=0)
                self.playersign = self.canvas.create_oval(200/self.frac, 200/self.frac, 200/self.frac+50/self.frac, 200/self.frac+50/self.frac, fill="red")
                # MiniZombie(self, 100, 100).draw(1, 1)
