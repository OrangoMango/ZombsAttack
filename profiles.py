from tkinter import *
import tkinter.ttk as t
import tkinter.simpledialog as s

import os, requests, json

class Profile:
        def __init__(self, home):
                self.home = home
                #print(os.getcwd())
                self.path = "/"+ os.getcwd().split("/")[1] + "/" + os.getcwd().split("/")[2] + "/"
                os.chdir(self.path)
                self.name = "Guest"
        def show_gui(self):
                self.id = self.home.canvas.create_text(400, 10, text=self.name)
                self.troph_id = self.home.canvas.create_text(30, 10, text="0")
        def ask_name(self):
                self.name = s.askstring("Enter name", "Enter name:")
        def create_profile_data(self):
                l = ["data.json"]
                for f in l:
                        with open(self.name+"/"+f, "w") as d:
                                json.dump(self.data, d, indent=4)
        def load_saves(self):
                if os.path.exists(self.name+"/"+"data.json"):
                        with open(self.name+"/"+"data.json") as f:
                                self.data = json.load(f)
                else:
                        self.data = {"Trophies" : 0}
                print(self.data)
        def config_name(self):
                if os.path.exists("profile.txt"):
                        with open("profile.txt") as f:
                                self.name = f.readline()
                else:
                        with open("profile.txt", "w") as f:
                                f.write(self.name)
        def create_profile_dir(self):
                if not os.path.exists(self.name):
                        os.mkdir(self.name)
                        self.create_profile_data()
        def set_asset(self):
                if not os.path.exists(".zombsAttack"):
                        tk = Tk()
                        tk.title("Loading data...")
                        self.ask_name()
                        done = 0
                        l = Label(tk, text="Loading... 0%")
                        l.grid()
                        tk.update()
                        p = t.Progressbar(tk, value=0)
                        p.grid(row=1)
                        tk.update()
                
                        os.mkdir(".zombsAttack")
                        os.chdir(self.path+".zombsAttack")
                        self.config_name()
                        self.create_profile_dir()
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
                        self.config_name()
                        self.load_saves()
