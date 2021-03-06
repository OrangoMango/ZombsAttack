import urllib.request, threading, time, requests, os, shutil, sys

from tkinter import *
from tkinter import messagebox
from zipfile import ZipFile
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
    def __init__(self, window, thread=True):
        self.window = window
        self.distribution = "Exe" if sys.argv[0].endswith(".exe") else "Winux"
        self.s = False
        if thread:
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
    def filter_for_dist():
        for v, t in self.data:
            if self.distribution == "Exe":
                pass                                      # Upgrade button
    def get_current_version(self):
        try:
            with open("version.txt") as f:
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
        if self.get_current_version() < max(self.get_tags()):
            return True
        else:
            return False
    def create_backup(self, version):
        oldpath = os.path.abspath(__file__+"/..")
        print(oldpath, os.path.abspath("."))

        if not os.path.exists("Backups"):
            os.mkdir("Backups")
        shutil.copytree(os.path.abspath("."), oldpath+"/.zombsAttack")
        shutil.make_archive("Backups/backup_{0}-{1}".format(version, time.strftime("%d%m%Y%H%M%S", time.localtime())), "zip", oldpath)
        shutil.rmtree(oldpath+"/.zombsAttack")
        print("Done")
    def upgrade(self, oldversion, newversion):
        oldpath = os.path.abspath(__file__+"/..")
        oldv, newv = oldversion, newversion
        vpath = "https://github.com/OrangoMango/ZombsAttack/archive/v{0}.zip".format(newv)
        if not os.path.exists("Versions"):
            os.mkdir("Versions")
        try:
            os.mkdir("Versions/{0}".format(newv))
        except:
            pass
        r = requests.get(vpath)
        open("Versions/{0}/{0}.zip".format(newv), "wb").write(r.content)
        z = ZipFile("Versions/{0}/{0}.zip".format(newv), "r")
        z.extractall(path="Versions/{0}/".format(newv))
        self.create_backup(oldv)
        for file in os.listdir("Versions/{0}/ZombsAttack-{0}".format(newv)):
            if file.endswith(".py"):
                shutil.copyfile("Versions/{0}/ZombsAttack-{0}/{1}".format(newv, file), oldpath+"/{0}".format(file))

        for image in os.listdir("Versions/{0}/ZombsAttack-{0}/Data/Images".format(newv)):
            shutil.copyfile("Versions/{0}/ZombsAttack-{0}/Data/Images/{1}".format(newv, image), "Data/Images/{0}".format(image))

        for language in os.listdir("Versions/{0}/ZombsAttack-{0}/Data/Languages".format(newv)):
            shutil.copyfile("Versions/{0}/ZombsAttack-{0}/Data/Languages/{1}".format(newv, language), "Data/Languages/{0}".format(language))

        shutil.copyfile("Versions/{0}/ZombsAttack-{0}/Data/Images/Loadingimage.gif".format(newv), "Data/Loadingimage.gif")

        with open("version.txt", "w") as f:
            f.write(str(newv))
            f.close()
    def show_gui(self):
        if not self.check():
            return
        tk = Tk()
        tk.title(self.window.profile.language_texts[37])

        def later():
            tk.destroy()

        def update():
            tk.destroy()
            
            messagebox.showinfo(self.window.profile.language_texts[37], self.window.profile.language_texts[41])
            
            self.upgrade(oldv, newv)
            
            ################################
            messagebox.showinfo(self.window.profile.language_texts[37], self.window.profile.language_texts[42])
            messagebox.showinfo(self.window.profile.language_texts[37], self.window.profile.language_texts[40])
            self.window.tk.destroy()
            sys.exit(0)
        
        oldv, newv = self.get_current_version(), max(self.get_tags())
        tk.bind("<FocusOut>", lambda e: tk.focus_force())
        Label(tk, text=self.window.profile.language_texts[35].format(newv), font="Calibri 12 bold", fg="blue").pack()
        Button(tk, text=self.window.profile.language_texts[38].format(newv), command=update, font="Calibri 10 bold").pack()
        Button(tk, text=self.window.profile.language_texts[39], command=later, font="Calibri 10 bold").pack()
