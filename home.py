from tkinter import *
import time, webbrowser

import profiles

class ScreenButton:
        def __init__(self, window):
                self.window = window
                self.id = None
                self.image = None
        def click(self, event):
                pass

class HelpButton(ScreenButton):
        def __init__(self, window):
                ScreenButton.__init__(self, window)
                self.image = PhotoImage(file="Data/Images/HelpButton.gif")
                self.id = self.window.canvas.create_image(250, 100, anchor="nw", image=self.image)
        def click(self, event):
                webbrowser.open("https://github.com/OrangoMango/ZombsAttack/wiki")

class PlayButton(ScreenButton):
        def __init__(self, window):
                ScreenButton.__init__(self, window)
                self.image = PhotoImage(file="Data/Images/PlayButton.gif")
                self.id = self.window.canvas.create_image(100, 100, anchor="nw", image=self.image)


class Window:
        def __init__(self):
                self.profile = profiles.Profile(self)
                self.profile.set_asset()
                self.tk = Tk()
                self.tk.title("ZombsAttack Lobby - OrangoMangoGames")
                self.canvas = Canvas(self.tk, width=500, height=300)
                self.canvas.pack()
                self.playbutton = PlayButton(self)
                self.helpbutton = HelpButton(self)

                self.canvas.create_rectangle(420, 80, 460, 120, fill="red")
                self.canvas.create_rectangle(420, 130, 460, 170, fill="red")
                self.canvas.create_rectangle(420, 180, 460, 220, fill="red")
                self.canvas.create_rectangle(100, 170, 350, 220, fill="red")
                
                self.canvas.tag_bind(self.playbutton.id, "<Button-1>", self.start)
                self.canvas.tag_bind(self.helpbutton.id, "<Button-1>", self.helpbutton.click)
                self.profile.show_gui()
                self.go = False
        def start(self, event):
                self.tk.quit()
                self.go = True
        def wait(self):
                while not self.go:
                        self.tk.update()
                        time.sleep(0.01)
