from tkinter import *

class MiniZombie:
        def __init__(self, minimap, rx, ry):
                x, y = int(rx/5), int(ry/5)
                self.minimap = minimap
                self.id = self.minimap.canvas.create_oval(x, y, x+50/5, y+50/5, fill="green")
        def draw(self, x, y):
                self.minimap.canvas.move(self.id, x/5, y/5)
        def delete(self):
                self.minimap.canvas.delete(self.id)

class MiniMap:
        def __init__(self, game):
                self.game = game
                self.canvas = Canvas(self.game.tk, width=100, height=100, bg="white")
                self.canvas.grid(column=1, row=0)
                self.playersign = self.canvas.create_oval(200/5, 200/5, 200/5+50/5, 200/5+50/5, fill="red")
                # MiniZombie(self, 100, 100).draw(1, 1)
