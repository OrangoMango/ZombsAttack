from tkinter import *
import tkinter.ttk as t
import tkinter.simpledialog as s

import os, requests, json, platform
import home

class Profile:
        def __init__(self, home):
                self.home = home
                self.path = "/"+ os.getcwd().split("/")[1] + "/" + os.getcwd().split("/")[2] + "/" #This line must be changed

                #print(platform.system()) #To know platform ('Linux' or 'Windows')
                #self.path = "C:/Users/bambini/"
                os.chdir(self.path)
                self.name = ""
                self.data = {"Trophies" : 0, "Brains" : 0, "Name" : self.name}
                self.language_texts = []
                self.LANGUAGE = "english"
                if not os.path.exists(".zombsAttack/Profiles"):
                        os.mkdir(".zombsAttack/Profiles")
        def get_leagues(self):
                l1, l2, l3, l4, l5, l6, l7, l8 = self.language_texts[12:20]
                t = self.data["Trophies"]

                # l1 t < 400
                # l2 t >= 400 and t < 1000
                # l3 t >= 1000 and t < 1500
                # l4 t >= 1500 and t < 2000
                # l5 t >= 2000 and t < 3000
                # l6 t >= 3000 and t < 5000
                # l7 t >= 5000 and t < 5800
                # l8 t >= 5800
                
                self.leagues = { l1 : t < 400,
                                 l2 : t >= 400 and t < 800,
                                 l3 : t >= 1000 and t < 1500,
                                 l4 : t >= 1500 and t < 2000,
                                 l5 : t >= 2000 and t < 3000,
                                 l6 : t >= 3000 and t < 5000,
                                 l7 : t >= 5000 and t < 5800,
                                 l8 : t >= 5800
                                }

                # l1 1
                # l2 5
                # l3 10
                # l4 20
                # l5 25
                # l6 30
                # l7 35
                # l8 40

                self.mtrophies = {
                                   l1 : 1,
                                   l2 : 5,
                                   l3 : 10,
                                   l4 : 20,
                                   l5 : 25,
                                   l6 : 30,
                                   l7 : 35,
                                   l8 : 40
                                }
                
                league = None
                for k, v in self.leagues.items():
                        if v:
                                league = k
                                break
                return league
                
        def load_languages(self):
                if os.path.exists("language.txt"):
                        with open("language.txt") as f:
                                self.LANGUAGE = f.readline()
                else:
                        with open("language.txt", "w") as f:
                                f.write(self.LANGUAGE)
                f.close()
                if not os.path.exists("Data/Languages"):
                        os.mkdir("Data/Languages")
                        for lanfile in ["italiano", "english"]:
                                r = requests.get("https://github.com/OrangoMango/ZombsAttack/raw/master/Data/Languages/{0}.txt".format(lanfile))
                                open("Data/Languages/{0}.txt".format(lanfile), "wb").write(r.content)

                LANGUAGE = self.LANGUAGE
                
                with open("Data/Languages/{0}.txt".format(LANGUAGE)) as f:
                        l = f.readlines()
                        for i in l:
                                self.language_texts.append(i.rstrip("\n"))
                self.current_league = self.get_leagues()
                
        def show_gui(self):
                self.id = home.ProfileButton(self.home, name=self.name).id
                self.id_x = None #TBD
                self.troph_id = self.home.canvas.create_text(30, 10, anchor="nw", text=self.data["Trophies"], font="Calibri 12 bold")
                self.troph_id_x = self.home.canvas.create_rectangle(25, 5, 135, 35)
                self.brains_id = self.home.canvas.create_text(160, 10, anchor="nw", text=self.data["Brains"], font="Calibri 12 bold")
                self.brains_id_x = self.home.canvas.create_rectangle(155, 5, 265, 35)
                self.league = self.home.canvas.create_rectangle(100, 5, 130, 35, fill="orange")
        def ask_name(self, firsttime=False):
                print(self.language_texts)
                n = self.name
                while self.name == "" or self.name == None or self.name in os.listdir():
                        if firsttime:
                                tk = Tk()
                                tk.title("ZombsAttack")
                                img = PhotoImage(file="Loadingimage.gif")
                                Label(tk, image=img).pack()
                        self.name = s.askstring(self.language_texts[1], self.language_texts[1]+":")
                        if firsttime:
                                tk.destroy()
                self.data["Name"] = self.name
                return n
        def create_profile_data(self):
                with open("Profiles/"+self.name+"/"+"data.json", "w") as d:
                         json.dump(self.data, d, indent=4)
        def load_saves(self):
                if os.path.exists("Profiles/"+self.name+"/"+"data.json"):
                        with open("Profiles/"+self.name+"/"+"data.json") as f:
                                self.data = json.load(f)
                #print(self.data) this prints current data dictionary
        def save_saves(self):
                        if os.path.exists("Profiles/"+self.name+"/"+"data.json"):
                                        with open("Profiles/"+self.name+"/"+"data.json", "w") as f:
                                                        json.dump(self.data, f, indent=4)
        def config_name(self, ft=False):
                if os.path.exists("profile.txt"):
                        with open("profile.txt") as f:
                                self.name = f.readline()
                else:
                        with open("profile.txt", "w") as f:
                                n = self.ask_name(ft)
                                f.write(self.name)
                                if n in os.listdir():
                                        return
                                else:
                                        self.create_profile_dir()
                f.close()
                if not os.path.exists("version.txt"):
                        with open("version.txt", "w") as f:
                                f.write(str(self.home.version))
                                f.close()
                if not os.path.exists("Bin_downloads"):
                        os.mkdir("Bin_downloads")
        def create_profile_dir(self):
                if not os.path.exists("Profiles/"+self.name):
                        os.mkdir("Profiles/"+self.name)
                        self.create_profile_data()
        def set_asset(self):
                if not os.path.exists(".zombsAttack"):
                        tk = Tk()
                        tk.title("Downloading data...")
                        os.mkdir(".zombsAttack")
                        os.chdir(self.path+".zombsAttack")
                        r = requests.get("https://github.com/OrangoMango/ZombsAttack/raw/master/Data/Images/Loadingimage.gif")
                        open("Loadingimage.gif", "wb").write(r.content)
                        done = 0
                        loadimage = PhotoImage(file="Loadingimage.gif", master=tk)
                        iml = Label(image=loadimage)
                        iml.pack()
                        l = Label(tk, text="Downloading languages... 0%")
                        l.pack()
                        p = t.Progressbar(tk, value=0)
                        p.pack()
                        tk.update()
                        if not os.path.exists("Data"):
                                os.mkdir("Data")
                                self.load_languages()
                                if not os.path.exists("Data/Images"):
                                        os.mkdir("Data/Images")
                                img = ["Map", "Minimap", "Player", "Player_E", "Player_N", "Player_W"] + ["Zombie_{0}".format(x) for x in range(1, 9)] + ["PlayButton", "HelpButton", "Language", "Settings", "Statistics", "Back", "Shop"]
                                for image in img:
                                        r = requests.get("https://github.com/OrangoMango/ZombsAttack/raw/master/Data/Images/{0}.gif".format(image))
                                        done += 1
                                        p.config(value=100/len(img)*done)
                                        l.config(text="Downloading {0}... {1}%".format(image+".gif", int(100/len(img)*done)))
                                        tk.update()
                                        open("Data/Images/{0}.gif".format(image), "wb").write(r.content)
                        
                        self.config_name()
                                        
                        tk.destroy()
                else:
                        os.chdir(self.path+".zombsAttack")
                        self.load_languages()
                        self.config_name(True)
                        self.load_saves()
