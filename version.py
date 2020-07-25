import urllib.request, threading, time

from tkinter import *
import tkinter.ttk as t

def th(ins):
    tk = Tk()
    tk.title(ins.window.profile.language_texts[36])
    Label(tk, text=ins.window.profile.language_texts[36]+"...").pack()
    p = t.Progressbar(tk, mode="indeterminate")
    p.pack()
    v = 0
    tk.update()
    while not ins.s:
        v += 20
        if v >= 100:
            v = 0
        p.config(value=v)
        tk.update()
        time.sleep(0.1)
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
        if True: #self.get_current_version() < max(self.get_tags()):
            return True
        else:
            return False
    def show_gui(self):
        if False: #self.get_current_version() < max(self.get_tags()):
            return
        tk = Tk()
        tk.title(self.window.profile.language_texts[37])
        
        def focus(e):
            time.sleep(0.15)
            tk.focus_force()

        def later():
            tk.destroy()
        
        oldv, newv = self.get_current_version(), max(self.get_tags())
        tk.bind("<FocusOut>", focus)
        Label(tk, text=self.window.profile.language_texts[35].format(newv), font="Calibri 12 bold", fg="blue").pack()
        Button(tk, text=self.window.profile.language_texts[38].format(newv), font="Calibri 10 bold").pack()
        Button(tk, text=self.window.profile.language_texts[39], command=later, font="Calibri 10 bold").pack()
