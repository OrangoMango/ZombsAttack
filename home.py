from tkinter import *
import time, webbrowser, os

import profiles

class ScreenButton:
        def __init__(self, window):
                self.window = window
                self.id = None
                self.image = None
        def click(self, event):
                print("Clicked")

class BackButton(ScreenButton):
        def __init__(self, *args):
                ScreenButton.__init__(self, *args)
                self.id = self.window.canvas.create_rectangle(30, 230, 120, 280, fill="lightgreen")
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

class LanguageButton(ScreenButton):
        def __init__(self, *args):
                ScreenButton.__init__(self, *args)
                self.id = self.window.canvas.create_rectangle(420, 130, 460, 170, fill="red")
                self.languages = [l.rpartition(".")[0] for l in os.listdir("Data/Languages")]
                self.backbutton = None
                self.languagesbuttons = []
        def click(self, event):
                bg = self.window.canvas.create_rectangle(0, 0, 500, 300, fill="yellow")
                x = 0
                self.backbutton = BackButton(self.window)
                self.window.canvas.tag_bind(self.backbutton.id, "<Button-1>", self.backbutton.click)
                self.backbutton.toback.append(bg)
                for language in self.languages:
                        self.backbutton.toback.append(self.window.canvas.create_rectangle(40+x, 40, 140+x, 90, fill="lightblue"))
                        self.backbutton.toback.append(self.window.canvas.create_text(57+x, 55, anchor="nw", text=language, font="Calibri 13"))
                        x += 100 + (20)
        def language_select(self):
                pass

class Window:
        def __init__(self):
                self.profile = profiles.Profile(self)
                self.profile.set_asset()
                self.tk = Tk()
                self.tk.title("ZombsAttack Lobby - OrangoMangoGames")
                self.canvas = Canvas(self.tk, width=500, height=300, bg="yellow")
                self.canvas.pack()
                self.playbutton = PlayButton(self)
                self.helpbutton = HelpButton(self)
                self.languagebutton = LanguageButton(self)

                self.canvas.create_rectangle(420, 80, 460, 120, fill="red")
                self.canvas.create_rectangle(420, 180, 460, 220, fill="red")
                self.canvas.create_rectangle(100, 170, 350, 220, fill="red")
                
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
