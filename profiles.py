from tkinter import *

class Profile:
        def __init__(self, home):     
                self.home = home
                self.id = self.home.canvas.create_text(400, 10, text="OrangoMango")
