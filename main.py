from tkinter import *
from tkinter import messagebox
import time, random

import maps, gstat, home

class Game:
        def __init__(self):
                #self.homewindow = home.Window()
                #self.homewindow.wait()
                self.tk = Tk()
                self.tk.title("ZombsAttack")
                self.canvas = Canvas(self.tk, width=500, height=500, bg="lightgray")
                self.canvas.grid(rowspan=2, column=0, row=0)
                self.background = PhotoImage(file="Map.gif")
                self.bg = self.canvas.create_image(0, 0, image=self.background, anchor="nw")
                self.minimap = maps.MiniMap(self)
                self.gamestats = gstat.Statistics(self)
                self.p_n = 0
                self.name = "OrangoMango"
                self.patrons = []
                self.zombies = []
                self.ftexts = []
                self.ftextsn = 0
                self.zombies_number = 0
        def mainloop(self):
                while True:
                        p.draw()
                        for zombie in self.zombies:
                                zombie.draw()
                        for pat in self.patrons:
                                pat.draw()
                        for ftext in self.ftexts:
                                ftext.draw()
                        self.tk.update()
                        if random.randint(1, 10000) <= 15:
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
        def gameover(self):
                messagebox.showerror("Game over", "GAME OVER")
                self.tk.destroy()

class FlowingText:
        def __init__(self, game, x, y, text="FlowingText - Class", tag=0):
                self.game = game
                self.text = text
                self.tag = tag
                self.id_x = self.game.canvas.create_text(x, y, text=self.text, font="Calibri 10 bold", tags="ftext#{0}".format(tag))
                self.id = "ftext#{0}".format(tag)
        def draw(self):
                self.game.canvas.move(self.id, 0, -2)
                p = self.game.canvas.coords(self.id)
                if p[1] <= 0:
                        self.delete()
        def delete(self):
                self.game.canvas.delete(self.id)
                for ft in self.game.ftexts:
                        if ft.tag == self.tag:
                                self.game.ftexts.remove(ft)
                                break
                

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
                self.images = [PhotoImage(file="Player.gif"), PhotoImage(file="Player_N.gif"), PhotoImage(file="Player_W.gif"), PhotoImage(file="Player_E.gif")]
                self.name = self.game.name
                self.id_x = self.game.canvas.create_image(200, 200, image=self.images[0], anchor="nw", tags="Player")
                self.id_y = self.game.canvas.create_text(225, 190, text=self.name, tags="Player")
                self.id = "Player"
                self.game.tk.bind("<KeyPress>", self.press)
                self.game.tk.bind("<KeyRelease>", self.release)
                self.life = 100
                self.timer = 0
                self.direction = "n"
                self.mx, self.my = 0, 0
                self.kills = 0
                self.damage = 0
                self.lifelabel = LifeLabel(self.game, self)
        def press(self, event):
                if event.char == "d":
                        #self.x = 3
                        self.mx, self.my = -3, 0
                        self.direction = "e"
                        self.game.canvas.itemconfig(self.id_x, image=self.images[3])
                elif event.char == "a":
                        #self.x = -3
                        self.mx, self.my = 3, 0
                        self.direction = "w"
                        self.game.canvas.itemconfig(self.id_x, image=self.images[2])
                elif event.char == "w":
                        self.mx, self.my = 0, 3
                        self.direction = "n"
                        self.game.canvas.itemconfig(self.id_x, image=self.images[1])
                elif event.char == "s":
                        self.mx, self.my = 0, -3
                        self.direction = "s"
                        self.game.canvas.itemconfig(self.id_x, image=self.images[0])
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
                self.mx, self.my = 0, 0
        def draw(self):
                '''self.game.canvas.move(self.id, self.x, self.y)
                self.game.canvas.move(self.lifelabel.id, self.x, self.y)
                self.game.canvas.move(self.lifelabel.labid, self.x, self.y)'''
                #print(self.direction)
                self.game.canvas.move(self.game.bg, self.mx, self.my)
                self.game.minimap.canvas.move(self.game.minimap.bg, self.mx/self.game.minimap.frac, self.my/self.game.minimap.frac)
                for z in self.game.zombies:
                        self.game.canvas.move(z.id, self.mx, self.my)
                        self.game.canvas.move(z.lifelabel.id, self.mx, self.my)
                        self.game.canvas.move(z.lifelabel.labid, self.mx, self.my)
                        z.minizombie.draw(self.mx, self.my)
                for p in self.game.patrons:
                        self.game.canvas.move(p.id, self.mx, self.my)
                self.timer -= 1
        def getCoord(self):
                pos = self.game.canvas.coords(self.id)
                return pos + [pos[0]+50, pos[1]+50]

class Zombie:
        def __init__(self, game, c, w, h, tag=0, initdirection="s"):
                self.game = game
                x, y = c
                self.selection = random.choice(["stay", "stax"])
                self.dx, self.dy = 0, 1
                self.life = 100
                self.tag = tag
                self.direction = initdirection
                #print(self.direction)
                #print(self.tag)
                self.id = self.game.canvas.create_rectangle(x, y, x+w, y+h, fill="green", tags="zombie_{0}".format(self.tag))
                self.lifelabel = LifeLabel(self.game, self, position="top")
                self.alivetimer = 0
                self.fromplayer = False
                self.minizombie = maps.MiniZombie(self.game.minimap, x, y)
        def draw(self):
                self.alivetimer += 1
                self.direction = self.getPlayerDTrack()
                if self.alivetimer >= 1500:
                        self.life -= 15
                        self.alivetimer = 1490
                        self.lifelabel.update()
                p = self.getCoord()
                if self.direction == "n":
                        self.dx, self.dy = 0, 1
                        statement = p[3] >= 500
                elif self.direction == "s":
                        self.dx, self.dy = 0, -1
                        statement = p[1] <= 0
                elif self.direction == "e":
                        self.dx, self.dy = 1, 0
                        statement = p[2] >= 500
                elif self.direction == "w":
                        self.dx, self.dy = -1, 0
                        statement = p[0] <= 0
                else:
                        print(self.direction)
                self.minizombie.draw(self.dx, self.dy)
                self.game.canvas.move(self.id, self.dx, self.dy)
                self.game.canvas.move(self.lifelabel.id, self.dx, self.dy)
                self.game.canvas.move(self.lifelabel.labid, self.dx, self.dy)
                
                playerg = self.game.player.getCoord()
                
                ############### CALCULATE COLLISION ###############
                
                if ((p[3] >= playerg[1] and p[3] <= playerg[3]) and (p[2] >= playerg[0] and p[2] <= playerg[2])) or  \
                    ((p[3] >= playerg[1] and p[3] <= playerg[3]) and (p[0] >= playerg[1] and p[0] <= playerg[3])) or \
                     ((p[1] >= playerg[1] and p[1] <= playerg[3]) and (p[0] >= playerg[0] and p[0] <= playerg[2])) or \
                     ((p[1] >= playerg[1] and p[1] <= playerg[3]) and (p[2] >= playerg[0] and p[2] <= playerg[2])): #QUI
                
                ############################################
                        self.game.canvas.move(self.id, (-self.dx)*15, (-self.dy)*15)
                        self.minizombie.draw((-self.dx)*15, (-self.dy)*15)
                        self.game.canvas.move(self.lifelabel.id, (-self.dx)*15, (-self.dy)*15)
                        self.game.canvas.move(self.lifelabel.labid, (-self.dx)*15, (-self.dy)*15)
                        if not self.game.player.life < 10:
                                self.game.player.life -= 10
                        else:
                                self.game.gameover()
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
                        self.die(self.fromplayer)
        def die(self, from_player=False):
                for i in self.game.zombies:
                        if i.tag == self.tag:
                                self.game.zombies.remove(i)
                                #print(len(self.game.zombies))
                                break
                p = self.getCoord()
                self.game.canvas.delete("zombie_{0}".format(self.tag))
                self.minizombie.delete()
                self.lifelabel.delete()
                if from_player:
                        self.game.player.kills += 1
                        self.game.gamestats.labels[0]["text"] = "Kills: {0}".format(self.game.player.kills)
                        #print(self.game.player.kills)
                        f = FlowingText(self.game, p[0]+(p[2]-p[0])/2, p[1]+(p[3]-p[1])/2, text="+1 Kill", tag=self.game.ftextsn)
                        self.game.ftextsn += 1
                        self.game.ftexts.append(f)
                zs = self.game.getZombieSpawn()
                z = Zombie(self.game, zs[0], 50, 50, tag=self.game.zombies_number, initdirection=zs[1])
                self.game.zombies_number += 1
                self.game.zombies.append(z)
        def getCoord(self):
                return self.game.canvas.coords(self.id)
        def getPlayerDTrack(self):
                player = self.game.player
                p = player.getCoord()
                zp = self.game.canvas.coords(self.id)
                centerp, centerzp = (p[0]+(p[2]-p[0])/2, p[1]+(p[3]-p[1])/2), (zp[0]+(zp[2]-zp[0])/2, zp[1]+(zp[3]-zp[1])/2)
                #print(p, zp, centerp, centerzp)
                
                stax = centerzp[0] <= centerp[0]
                stax2 = centerp[0] == centerzp[0]
                
                stay = centerp[1] <= centerzp[1]
                stay2 = centerp[1] == centerzp[1]
                
                
                def reversedir():
                        d = self.direction
                        if d == "n":
                                return "s"
                        elif d == "s":
                                return "n"
                        elif d == "w":
                                return "e"
                        elif d == "e":
                                return "w"
                
                statement = self.selection
                
                if eval(statement):
                        direction = "e"
                        if eval(statement+"2"):
                                if eval("stay" if self.selection == "stax" else "stay"):
                                        direction = "s"
                                        if eval("stay"+"2" if self.selection == "stax" else "stay"+"2"):
                                                direction = reversedir()
                                else:
                                        direction = "n"
                        else:
                                pass
                else:
                        direction = "w"
                        if eval(statement+"2"):
                                if eval("stay" if self.selection == "stax" else "stay"):
                                        direction = "s"
                                        if eval("stay"+"2" if self.selection == "stax" else "stay"+"2"):
                                                direction = reversedir()
                                else:
                                        direction = "n"
                        else:
                                pass
               # print(direction)
               # time.sleep(0.05)
                return direction

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
                                       self.player.damage += 15
                                       self.game.gamestats.labels[1]["text"] = "Damage: {0}".format(self.player.damage)
                                       zombie.lifelabel.update()
                                       self.delete()
                                       if zombie.life <= 0:
                                                zombie.fromplayer = True
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
        #g.mainloop()
        try:
                g.mainloop()
        except Exception as e:
                print("Program end %s" % e)
