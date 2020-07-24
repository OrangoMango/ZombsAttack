import urllib.request, threading, time

from tkinter import *


def th(ins):
    tk = Tk()
    tk.title(ins.window.profile.language_texts[36])
    Label(tk, text=ins.window.profile.language_texts[36]).pack()
    tk.update()
    while not ins.s:
        pass
    tk.destroy()

class Version:
    def __init__(self, window):
        self.window = window
        self.s = False
        t = threading.Thread(target=th, args=(self,))
        t.start()
        r = urllib.request.urlopen("https://github.com/OrangoMango/ZombsAttack/releases")

        self.versions = []

        for i in r.readlines():
            if "ZombsAttack" and "v" and "<a href=\"/OrangoMango/ZombsAttack/releases/tag" in str(i):
                self.versions.append(str(i))
        self.data = []
        self.s = True
    def get_data(self):
        self.data = []
        for p in self.versions:
            self.data.append((p.split(">")[1].split("<")[0], p.split(">")[1].split("<")[0].split("v")[1]))
        return self.data
    def get_current_version(self):
        try:
            with open("/home/paul/.zombsAttack/version.txt") as f:
                d = f.read()
                f.close()
                return float(d)
        except:
            raise FileNotFoundError("Could not open file \"version.txt\"")
    def get_tags(self):
        if not self.data:
            raise ValueError("No data available")
        d = []
        for x in self.data:
            d.append(float(x[1]))
        return d
    def get_names(self):
        if not self.data:
            raise ValueError("No data available")
        d = []
        for x in self.data:
            d.append(x[0])
        return d
    def check(self):
        if True: #self.get_current_version() < max(self.get_tags()): Temporaneamente
            return True
        else:
            return False
    def show_gui(self):
        tk = Tk()
        tk.title(self.window.profile.language_texts[35])
        
        def focus(e):
            time.sleep(0.15)
            tk.focus_force()
            
        tk.bind("<FocusOut>", focus)
        Label(tk, text=self.window.profile.language_texts[35]).pack()
