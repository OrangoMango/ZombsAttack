from tkinter import *

class Game:
        def __init__(self):
                self.tk = Tk()
                self.canvas = Canvas(self.tk, width=500, height=500, bg="lightgreen")
                self.canvas.pack()

        def mainloop(self):
                self.tk.mainloop()

class Player:
        def __init__(self, game):
                self.game = game
                self.id = self.game.canvas.create_rectangle(225, 440, 275, 490, fill="red")

if __name__ == "__main__":
        g = Game()
        p = Player(g)
        g.mainloop()
