from tkinter import *
import time

class Game:
        def __init__(self):
                self.tk = Tk()
                self.tk.title("ZombsAttack")
                self.canvas = Canvas(self.tk, width=500, height=500, bg="lightgreen")
                self.canvas.pack()
                self.p_n = 0
                self.patrons = []
        def mainloop(self):
                while True:
                        p.draw()
                        for pat in self.patrons:
                                pat.draw()
                        self.tk.update()
                        time.sleep(0.01)

class LifeLabel:
        def __init__(self, game, player):
                self.game = game
                self.player = player
                ppos = self.game.canvas.coords(self.player.id)
                px, py, px1, py1 = ppos[0], ppos[1], ppos[2], ppos[3]
                x, y, x1, y1 = px-10, py1+5, px+60, py1+5+10
                self.id = self.game.canvas.create_rectangle(x, y, x1, y1, fill="green", width=2)
                self.value = self.player.life
        def getColorValue(self):
                pass

class Player:
        def __init__(self, game):
                self.game = game
                self.x, self.y = 0, 0
                self.id = self.game.canvas.create_rectangle(225, 430, 275, 480, fill="red")
                self.game.tk.bind("<KeyPress>", self.press)
                self.game.tk.bind("<KeyRelease>", self.release)
                self.life = 100
                self.timer = 0
                self.lifelabel = LifeLabel(self.game, self)
        def press(self, event):
                if event.char == "d":
                        self.x = 3
                elif event.char == "a":
                        self.x = -3
                elif event.keysym == "space":
                        if self.timer < 0:
                                self.shoot()
                                self.timer = 10
                else:
                        print(event.char, event.keysym)
        def shoot(self):
                p = Patron(self.game, self, tag=self.game.p_n)
                self.game.patrons.append(p)
                self.game.p_n += 1
                #print(self.game.p_n)
        def release(self, event):
                self.x = 0
        def draw(self):
                self.game.canvas.move(self.id, self.x, self.y)
                self.game.canvas.move(self.lifelabel.id, self.x, self.y)
                self.timer -= 1

class Patron:
        def __init__(self, game, player, tag=0):
                self.game = game
                self.player = player
                self.tag = tag
                pl_pos = self.game.canvas.coords(self.player.id)
                x, y, x1, y1 = pl_pos[0]+((pl_pos[2]-pl_pos[0])/2), pl_pos[1]-30, pl_pos[0]+((pl_pos[2]-pl_pos[0])/2), pl_pos[1]-5
                self.id = self.game.canvas.create_line(x, y, x1, y1, width=10, tags="patron_{0}".format(self.tag))
        def draw(self):
                self.game.canvas.move(self.id, 0, -5)
                pos = self.game.canvas.coords(self.id)
                #print(self.game.patrons)
                if pos[1] < 0:
                        for i in self.game.patrons:
                                if i.tag == self.tag:
                                        self.game.patrons.remove(i)
                                        break
                        self.game.canvas.delete("patron_{0}".format(self.tag))

if __name__ == "__main__":
        g = Game()
        p = Player(g)
        #LifeLabel(g, p)
        try:
                g.mainloop()
        except Exception as e:
                print("Program end %s" % e)
