from tkinter import *

class MiniZombie:
        def __init__(self, minimap, rx, ry):
                x, y = int(rx/5), int(ry/5)
                self.minimap = minimap
                self.id = self.minimap.canvas.create_oval(x, y, x+50/5, y+50/5, fill="green")
        def draw(self, x, y):
                nx, ny = int(x/5) if x != 1 else int(x/5), int(y/5) if y != 1 else int(y/5)
                self.minimap.canvas.move(self.id, int(x/5), int(y/5))
                self.minimap.game.tk.update()

class MiniMap:
        def __init__(self, game):
                self.game = game
                self.canvas = Canvas(self.game.tk, width=100, height=100, bg="white")
                self.canvas.grid(column=1, row=0)
                self.playersign = self.canvas.create_oval(200/5, 200/5, 200/5+50/5, 200/5+50/5, fill="red")
                self.zombssigns = []
                #MiniZombie(self, 100, 100).draw(1, 1)
