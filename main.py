from tkinter import *
import time, random

class Game:
        def __init__(self):
                self.tk = Tk()
                self.tk.title("ZombsAttack")
                self.canvas = Canvas(self.tk, width=500, height=500, bg="lightgray")
                self.canvas.pack()
                self.p_n = 0
                self.patrons = []
                self.zombies = []
                self.zombies_number = 0
        def mainloop(self):
                while True:
                        p.draw()
                        for zombie in self.zombies:
                                zombie.draw()
                        for pat in self.patrons:
                                pat.draw()
                        self.tk.update()
                        if random.randint(1, 10000) <= 19:
                                zs = self.getZombieSpawn()
                                z = Zombie(self, zs[0], 50, 50, tag=self.zombies_number, initdirection=zs[1])
                                self.zombies_number += 1
                                self.zombies.append(z)
                        time.sleep(0.01)
        def getZombieSpawn(self):
                side = random.choice(["n", "s", "e", "w"])
                if side == "n":
                        return (random.randint(20, 420), -90), side
                elif side == "s":
                        return (random.randint(20, 420), 590), side
                elif side == "w":
                        return (-90, random.randint(20, 420)), side
                elif side == "e":
                        return (590, random.randint(20, 420)), side

class LifeLabel:
        def __init__(self, game, player, position="bottom"):
                self.game = game
                self.player = player
                ppos = self.player.getCoord()
                px, py, px1, py1 = ppos[0], ppos[1], ppos[2], ppos[3]
                if position == "bottom":
                        x, y, x1, y1 = px-10, py1+5, px+60, py1+5+10
                elif position == "top":
                        x, y, x1, y1 = px-10, py-15, px+60, py-15+10
                else:
                        raise ValueError("Positions are only top and bottom")
                self.position = position
                self.value = self.player.life
                self.id = self.game.canvas.create_rectangle(x, y, x1, y1, width=2)
                self.labid = self.game.canvas.create_rectangle(x, y, x+self.getCoordValue()-1, y1-1, fill=self.getColorValue())
        def getColorValue(self):
                # red, orange, yellow, lightgreen, green
                if self.value <= 20:
                        return "red"
                elif self.value <= 40:
                        return "orange"
                elif self.value <= 60:
                        return "yellow"
                elif self.value <= 80:
                        return "lightgreen"
                elif self.value <= 100:
                        return "green"
        def getCoordValue(self):
                # percentage
                return int(70/100*self.value)
        def update(self):
                self.game.canvas.delete(self.id)
                self.game.canvas.delete(self.labid)
                ppos = self.player.getCoord()
                px, py, px1, py1 = ppos[0], ppos[1], ppos[2], ppos[3]
                position = self.position
                if position == "bottom":
                        x, y, x1, y1 = px-10, py1+5, px+60, py1+5+10
                elif position == "top":
                        x, y, x1, y1 = px-10, py-15, px+60, py-15+10
                else:
                        raise ValueError("Positions are only top and bottom")
                self.value = self.player.life
                self.id = self.game.canvas.create_rectangle(x, y, x1, y1, width=2)
                self.labid = self.game.canvas.create_rectangle(x, y, x+self.getCoordValue()-1, y1-1, fill=self.getColorValue())
        def delete(self):
                self.game.canvas.delete(self.id)
                self.game.canvas.delete(self.labid)

class Player:
        def __init__(self, game):
                self.game = game
                self.image = PhotoImage(file="Player.gif")
                self.id = self.game.canvas.create_image(200, 200, image=self.image, anchor="nw")
                self.game.tk.bind("<KeyPress>", self.press)
                self.game.tk.bind("<KeyRelease>", self.release)
                self.life = 100
                self.timer = 0
                self.direction = "n"
                self.mx, self.my = 0, 0
                self.lifelabel = LifeLabel(self.game, self)
        def press(self, event):
                if event.char == "d":
                        #self.x = 3
                        self.mx, self.my = -3, 0
                        self.direction = "e"
                elif event.char == "a":
                        #self.x = -3
                        self.mx, self.my = 3, 0
                        self.direction = "w"
                elif event.char == "w":
                        self.mx, self.my = 0, 3
                        self.direction = "n"
                elif event.char == "s":
                        self.mx, self.my = 0, -3
                        self.direction = "s"
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
                '''if self.life >= 5:
                        self.life -= 5
                else:
                        self.life = 100
                self.lifelabel.update()'''
                #print(self.game.p_n)
        def release(self, event):
                self.mx, self.my = 0, 0
        def draw(self):
                '''self.game.canvas.move(self.id, self.x, self.y)
                self.game.canvas.move(self.lifelabel.id, self.x, self.y)
                self.game.canvas.move(self.lifelabel.labid, self.x, self.y)'''
                #print(self.direction)
                for z in self.game.zombies:
                        self.game.canvas.move(z.id, self.mx, self.my)
                        self.game.canvas.move(z.lifelabel.id, self.mx, self.my)
                        self.game.canvas.move(z.lifelabel.labid, self.mx, self.my)
                for p in self.game.patrons:
                        self.game.canvas.move(p.id, self.mx, self.my)
                self.timer -= 1
        def getCoord(self):
                pos = self.game.canvas.coords(self.id)
                return pos + [pos[0]+50, pos[1]+50]

class Zombie:
        def __init__(self, game, c, w, h, tag=0, initdirection="s"):
                self.game = game
                x, y = c[0], c[1]
                self.dx, self.dy = 0, 1
                self.life = 100
                self.tag = tag
                self.direction = initdirection
                print(self.direction)
                #print(self.tag)
                self.id = self.game.canvas.create_rectangle(x, y, x+w, y+h, fill="green", tags="zombie_{0}".format(self.tag))
                self.lifelabel = LifeLabel(self.game, self, position="top")
        def draw(self):
                p = self.getCoord()
                if self.direction == "n":
                        self.dx, self.dy = 0, 1
                        statement = p[3] >= 500
                elif self.direction == "s":
                        self.dx, self.dy = 0, -1
                        statement = p[1] <= 0
                elif self.direction == "w":
                        self.dx, self.dy = 1, 0
                        statement = p[2] >= 500
                elif self.direction == "e":
                        self.dx, self.dy = -1, 0
                        statement = p[0] <= 0
                self.game.canvas.move(self.id, self.dx, self.dy)
                self.game.canvas.move(self.lifelabel.id, self.dx, self.dy)
                self.game.canvas.move(self.lifelabel.labid, self.dx, self.dy)
                
                playerg = self.game.player.getCoord()
                
                ############### CALCULATE COLLISION ###############
                
                if ((p[3] >= playerg[1] and p[3] <= playerg[3]) and (p[2] >= playerg[0] and p[2] <= playerg[2])) or  \
                    ((p[3] >= playerg[1] and p[3] <= playerg[3]) and (p[0] >= playerg[1] and p[0] <= playerg[3])) or \
                     False or \
                     False: #QUI
                
                ############################################
                        self.game.canvas.move(self.id, 0, -15)
                        self.game.canvas.move(self.lifelabel.id, 0, -15)
                        self.game.canvas.move(self.lifelabel.labid, 0, -15)
                        self.life -= 15
                        self.lifelabel.update()
                        if not self.game.player.life < 10:
                                self.game.player.life -= 10
                        else:
                                self.game.player.life = 100
                        self.game.player.lifelabel.update()
                if statement:
                        self.game.canvas.move(self.id, (-self.dx)*15, (-self.dy)*15)
                        self.game.canvas.move(self.lifelabel.id, (-self.dx)*15, (-self.dy)*15)
                        self.game.canvas.move(self.lifelabel.labid, (-self.dx)*15, (-self.dy)*15)
                        self.life -= 15
                        self.lifelabel.update()
                if not p:
                        return
                if self.life <= 0:
                        self.die()
        def die(self):
                for i in self.game.zombies:
                        if i.tag == self.tag:
                                self.game.zombies.remove(i)
                                #print(len(self.game.zombies))
                                break
                self.game.canvas.delete("zombie_{0}".format(self.tag))
                self.lifelabel.delete()
                zs = self.game.getZombieSpawn()
                z = Zombie(self.game, zs[0], 50, 50, tag=self.game.zombies_number, initdirection=zs[1])
                self.game.zombies_number += 1
                self.game.zombies.append(z)
        def getCoord(self):
                return self.game.canvas.coords(self.id)

class Patron:
        def __init__(self, game, player, tag=0):
                self.game = game
                self.player = player
                self.tag = tag
                pl_pos = self.player.getCoord()
                if self.player.direction == "n":
                        x, y, x1, y1 = pl_pos[0]+((pl_pos[2]-pl_pos[0])/2)-2, pl_pos[1]-30, pl_pos[0]+((pl_pos[2]-pl_pos[0])/2)+2, pl_pos[1]-5
                        self.yd = -5
                        self.xd = 0
                elif self.player.direction == "s":
                        x, y, x1, y1 = pl_pos[1]+((pl_pos[3]-pl_pos[1])/2)-2, pl_pos[2]+30, pl_pos[1]+((pl_pos[3]-pl_pos[1])/2)+2, pl_pos[2]+5
                        self.yd = 5
                        self.xd = 0
                elif self.player.direction == "e":
                        x, y, x1, y1 = pl_pos[2]+2, pl_pos[1]+((pl_pos[3]-pl_pos[1])/2)-5, pl_pos[2]+5+25, pl_pos[1]+((pl_pos[3]-pl_pos[1])/2)+2
                        self.xd = 5
                        self.yd = 0
                elif self.player.direction == "w":
                        x, y, x1, y1 = pl_pos[0]-2-25, pl_pos[1]+((pl_pos[3]-pl_pos[1])/2)-5, pl_pos[0]-5, pl_pos[1]+((pl_pos[3]-pl_pos[1])/2)+2
                        self.xd = -5
                        self.yd = 0
                else:
                        raise ValueError("Invalid direction given")
                self.id = self.game.canvas.create_rectangle(x, y, x1, y1, width=10, tags="patron_{0}".format(self.tag))
        def draw(self):
                pos = self.game.canvas.coords(self.id)
                if pos[1] < 0:
                        self.delete()
                for zombie in self.game.zombies:
                       z_pos = zombie.getCoord()
                       if not z_pos:
                                continue
                       #print(pos, z_pos)
                       if pos[1] >= z_pos[1] and pos[1] <= z_pos[3]:
                               if pos[0] >= z_pos[0] and pos[0] <= z_pos[2]:
                                       zombie.life -= 15
                                       zombie.lifelabel.update()
                                       self.delete()
                                       break
                self.game.canvas.move(self.id, self.xd, self.yd)
                #print(self.game.patrons)
        def delete(self):
                for i in self.game.patrons:
                        if i.tag == self.tag:
                                self.game.patrons.remove(i)
                                break
                self.game.canvas.delete("patron_{0}".format(self.tag))

if __name__ == "__main__":
        g = Game()
        p = Player(g)
        g.player = p
        z = Zombie(g, (20, -90), 50, 50, tag=g.zombies_number)
        g.zombies_number += 1
        g.zombies.append(z)
        g.mainloop()
       # try:
        #         g.mainloop()
       # except Exception as e:
         #      print("Program end %s" % e)
