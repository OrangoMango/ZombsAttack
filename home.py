from tkinter import *
import time, webbrowser

class HelpButton:
        def __init__(self, window):
                self.window = window
                self.id = self.window.canvas.create_rectangle(250, 100, 350, 150, fill="blue")
        def click(self, event):
                webbrowser.open("https://github.com/OrangoMango/ZombsAttack/wiki")

class PlayButton:
        def __init__(self, window):
                self.window = window
                self.id = self.window.canvas.create_rectangle(100, 100, 200, 150, fill="red")


class Window:
        def __init__(self):
                self.tk = Tk()
                self.tk.title("ZombsAttack Lobby - OrangoMangoGames")
                self.canvas = Canvas(self.tk, width=500, height=300)
                self.canvas.pack()
                self.playbutton = PlayButton(self)
                self.helpbutton = HelpButton(self)
                import profiles; profiles.Profile(self)
                self.canvas.tag_bind(self.playbutton.id, "<Button-1>", self.start)
                self.canvas.tag_bind(self.helpbutton.id, "<Button-1>", self.helpbutton.click)
                self.go = False
        def start(self, event):
                self.tk.destroy()
                self.go = True
        def wait(self):
                self.tk.mainloop()
                if self.go:
                        self.tk.quit()
