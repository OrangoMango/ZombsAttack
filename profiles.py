from tkinter import *
import tkinter.ttk as t

import os, requests

class Profile:
        def __init__(self, home):
                self.home = home
                #print(os.getcwd())
                self.path = "/"+ os.getcwd().split("/")[1] + "/" + os.getcwd().split("/")[2] + "/"
                os.chdir(self.path)
        def show_gui(self):
                self.id = self.home.canvas.create_text(400, 10, text="OrangoMango")
        def set_asset(self):
                if not os.path.exists(".zombsAttack"):
                        tk = Tk()
                        tk.title("Loading data...")
                        done = 0
                        l = Label(tk, text="Loading... 0%")
                        l.grid()
                        tk.update()
                        p = t.Progressbar(tk, value=0)
                        p.grid(row=1)
                        tk.update()
                
                        os.mkdir(".zombsAttack")
                        os.chdir(self.path+".zombsAttack")
                        if not os.path.exists("Data"):
                                os.mkdir("Data")
                                if not os.path.exists("Data/Images"):
                                        os.mkdir("Data/Images")
                                img = ["Map", "Minimap", "Player", "Player_E", "Player_N", "Player_W"]
                                for image in img:
                                        r = requests.get("https://github.com/OrangoMango/ZombsAttack/raw/master/Data/Images/{0}.gif".format(image))
                                        done += 1
                                        p.config(value=100/len(img)*done)
                                        l.config(text="Loading... {0}%".format(int(100/len(img)*done)))
                                        tk.update()
                                        open("Data/Images/{0}.gif".format(image), "wb").write(r.content)
                                        
                                tk.destroy()
                else:
                        os.chdir(self.path+".zombsAttack")
