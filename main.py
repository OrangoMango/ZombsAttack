from tkinter import *
import time

class Game:
        def __init__(self):
                self.tk = Tk()
                self.tk.title("ZombsAttack")
                self.canvas = Canvas(self.tk, width=500, height=500, bg="lightgreen")
                self.canvas.pack()

        def mainloop(self):
                while True:
                        p.draw()
                        self.tk.update()
                        time.sleep(0.01)

class Player:
        def __init__(self, game):
                self.game = game
                self.x, self.y = 0, 0
                self.id = self.game.canvas.create_rectangle(225, 440, 275, 490, fill="red")
                self.game.tk.bind("<KeyPress>", self.press)
                self.game.tk.bind("<KeyRelease>", self.release)
        def press(self, event):
                if event.char == "d":
                        self.x = 3
                elif event.char == "a":
                        self.x = -3
        def release(self, event):
                self.x = 0
        def draw(self):
                self.game.canvas.move(self.id, self.x, self.y)

if __name__ == "__main__":
        g = Game()
        p = Player(g)
        g.mainloop()
