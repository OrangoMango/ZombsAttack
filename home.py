from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import time, webbrowser, os, sys, pickle

import profiles, main

class ScreenButton:
        def __init__(self, window):
                self.window = window
                self.id = None
                self.image = None
                self.bg = None
        def click(self, event):
                self.bg = self.window.canvas.create_rectangle(0, 0, 500, 300, fill="yellow")
                self.backbutton = BackButton(self.window)
                self.backbutton.toback.append(self.bg)

class ProfileButton(ScreenButton):
        def __init__(self, *args, name="Guest"):
                ScreenButton.__init__(self, *args)
                self.name = name
                self.id = self.window.canvas.create_text(400, 20, text=self.name, font="Calibri 12")
                self.window.canvas.tag_bind(self.id, "<Button-1>", self.click)
        def click(self, event):
                ScreenButton.click(self, event)
                self.frame = LabelFrame(self.window.tk, text=self.window.profile.language_texts[20])
                wf = self.window.canvas.create_window(30, 90, window=self.frame, anchor="nw")
                Label(self.frame, text=self.window.profile.language_texts[21]+": {0}".format(self.name)).grid()
                Label(self.frame, text=self.window.profile.language_texts[22]+":").grid(row=1)
                Button(self.frame, text=self.window.profile.language_texts[23], command=self.download_profile).grid(column=1, row=1)
                self.backbutton.toback.append(wf)
                ############################################
                self.frame2 = LabelFrame(self.window.tk, text=self.window.profile.language_texts[25])
                wf2 = self.window.canvas.create_window(300, 90, window=self.frame2, anchor="nw")
                Label(self.frame2, text="Ciao").pack()
        def download_profile(self):
                path = filedialog.asksaveasfilename(filetypes=[(".bin BinaryFile", "*.bin")])
                f = open(path, "wb")
                pickle.dump(self.window.profile.data, f)
                messagebox.showinfo(self.window.profile.language_texts[20], self.window.profile.language_texts[24])

class BackButton(ScreenButton):
        def __init__(self, *args):
                ScreenButton.__init__(self, *args)
                self.image = PhotoImage(file="Data/Images/Back.gif")
                self.id = self.window.canvas.create_image(30, 230, image=self.image, anchor="nw")
                self.window.canvas.tag_bind(self.id, "<Button-1>", self.click)
                self.toback = []
        def click(self, event):
                for i in self.toback:
                        self.window.canvas.delete(i)
                self.window.canvas.delete(self.id)
                self.toback = []

class HelpButton(ScreenButton):
        def __init__(self, *args):
                ScreenButton.__init__(self, *args)
                self.image = PhotoImage(file="Data/Images/HelpButton.gif")
                self.id = self.window.canvas.create_image(250, 100, anchor="nw", image=self.image)
        def click(self, event):
                webbrowser.open("https://github.com/OrangoMango/ZombsAttack/wiki")

class PlayButton(ScreenButton):
        def __init__(self, *args):
                ScreenButton.__init__(self, *args)
                self.image = PhotoImage(file="Data/Images/PlayButton.gif")
                self.id = self.window.canvas.create_image(100, 100, anchor="nw", image=self.image)

class SettingsButton(ScreenButton):
        def __init__(self, *args):
                ScreenButton.__init__(self, *args)
                self.image = PhotoImage(file="Data/Images/Settings.gif")
                self.id = self.window.canvas.create_image(420, 180, anchor="nw", image=self.image)
                self.window.canvas.tag_bind(self.id, "<Button-1>", self.click)
        def click(self, event):
                ScreenButton.click(self, event)

class StatisticsButton(ScreenButton):
        def __init__(self, *args):
                ScreenButton.__init__(self, *args)
                self.image = PhotoImage(file="Data/Images/Statistics.gif")
                self.id = self.window.canvas.create_image(420, 80, anchor="nw", image=self.image)
                self.window.canvas.tag_bind(self.id, "<Button-1>", self.click)
        def click(self, event):
                ScreenButton.click(self, event)

class ShopButton(ScreenButton):
        def __init__(self, *args):
                ScreenButton.__init__(self, *args)
                self.image = PhotoImage(file="Data/Images/Shop.gif")
                self.id = self.window.canvas.create_image(100, 170, anchor="nw", image=self.image)
                self.window.canvas.tag_bind(self.id, "<Button-1>", self.click)
        def click(self, event):
                ScreenButton.click(self, event)

class LanguageSelectButton:
        def __init__(self, window, x, y, x1, y1, language, tx, ty):
                self.window = window
                self.language = language
                self.id = "LanguageSelect#{0}".format(language)
                self.id_x = self.window.canvas.create_rectangle(x, y, x1, y1, fill="lightblue", tags=self.id)
                self.id_y = self.window.canvas.create_text(tx, ty, anchor="nw", text=language, font="Calibri 13", tags=self.id)
                self.window.canvas.tag_bind(self.id, "<Button-1>", self.click)
        def click(self, event):
                if self.window.profile.LANGUAGE == self.language:
                        messagebox.showerror(self.window.profile.language_texts[8], self.window.profile.language_texts[10])
                        return
                messagebox.showinfo(self.window.profile.language_texts[8], self.window.profile.language_texts[9].format(self.language))
                os.remove("language.txt")
                self.window.profile.LANGUAGE = self.language
                self.window.profile.config_name()
                self.window.tk.destroy()
                main.main()

class LanguageButton(ScreenButton):
        def __init__(self, *args):
                ScreenButton.__init__(self, *args)
                self.image = PhotoImage(file="Data/Images/Language.gif")
                self.id = self.window.canvas.create_image(420, 130, image=self.image, anchor="nw")
                self.languages = [l.rpartition(".")[0] for l in os.listdir("Data/Languages")]
                self.backbutton = None
                self.languagesbuttons = []
        def click(self, event):
                self.bg = self.window.canvas.create_rectangle(0, 0, 500, 300, fill="yellow")
                x = 0
                y = 0
                self.backbutton = BackButton(self.window)
                self.backbutton.toback.append(self.bg)
                for language in self.languages:
                        self.backbutton.toback.append(LanguageSelectButton(self.window, 40+x, 40+y, 140+x, 90+y, language, 57+x, 55+y).id)
                        x += 100 + (20)
                        if x == 120 * 3:
                                y += 50 + (20)
                                x = 0

class Window:
        def __init__(self):
                self.version = 5.0
                self.profile = profiles.Profile(self)
                try:
                        self.profile.set_asset()
                except:
                        messagebox.showerror("Error", "Internet Error, please verify your connection!")
                        os.rmdir("../.zombsAttack")
                        sys.exit()
                self.tk = Tk()
                self.tk.resizable(0, 0)
                self.tk.title("ZombsAttack Lobby - OrangoMangoGames")
                self.canvas = Canvas(self.tk, width=500, height=300, bg="yellow")
                self.canvas.pack()
                self.canvas.create_text(3, 285, font="Calibri 6 bold", anchor="nw", text="Game made by OrangoMango (Paul Kocian, SCRIPT) and Dado14 (Andrea Pintus, DESIGN) v{0} (C) 2020".format(self.version))
                self.playbutton = PlayButton(self)
                self.helpbutton = HelpButton(self)
                self.languagebutton = LanguageButton(self)
                self.settingsbutton = SettingsButton(self)
                self.statisticsbutton = StatisticsButton(self)
                self.shopbutton = ShopButton(self)
                
                self.canvas.tag_bind(self.playbutton.id, "<Button-1>", self.start)
                self.canvas.tag_bind(self.helpbutton.id, "<Button-1>", self.helpbutton.click)
                self.canvas.tag_bind(self.languagebutton.id, "<Button-1>", self.languagebutton.click)
                self.profile.show_gui()
                self.go = False
        def start(self, event):
                self.tk.quit()
                self.go = True
        def wait(self):
                while not self.go:
                        self.tk.update()
                        time.sleep(0.01)
