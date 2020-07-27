from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import time, webbrowser, os, sys, pickle, json, shutil

import profiles, main, version

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
                self.frame = LabelFrame(self.window.tk, text=self.window.profile.language_texts[20], bg="yellow")
                wf = self.window.canvas.create_window(110, 10, window=self.frame, anchor="nw")
                Label(self.frame, text=self.window.profile.language_texts[21]+": {0}".format(self.name), bg="yellow").grid()
                Label(self.frame, text=self.window.profile.language_texts[22]+":", bg="yellow").grid(row=1)
                Button(self.frame, text=self.window.profile.language_texts[23], command=self.download_profile, bg="red").grid(column=1, row=1)
                self.backbutton.toback.append(wf)
                ############################################
                self.frame2 = LabelFrame(self.window.tk, text=self.window.profile.language_texts[25], bg="yellow")
                wf2 = self.window.canvas.create_window(110, 90, window=self.frame2, anchor="nw")
                self.backbutton.toback.append(wf2)
                profiles_available = []
                for f in os.listdir("Profiles"):
                        profiles_available.append(f)
                radiobuttons = []
                self.select = StringVar(master=self.window.tk)
                self.select.set(self.name)

                def update_text_button():
                        self.selection_button.config(text=self.window.profile.language_texts[26]+" \"{0}\"".format(self.select.get()))
                        self.deletion_button.config(text=self.window.profile.language_texts[30]+" \"{0}\"".format(self.select.get()))
                
                for profile in profiles_available:
                        r = Radiobutton(self.frame2, text=profile, variable=self.select, value=profile, command=update_text_button, bg="yellow4")
                        r.grid(row=profiles_available.index(profile))
                        radiobuttons.append(r)
                self.selection_button = Button(self.frame2, text=self.window.profile.language_texts[26]+" \"{0}\"".format(self.select.get()), bg="red", command=self.select_profile)
                self.selection_button.grid(row=len(profiles_available))
                self.deletion_button = Button(self.frame2, text=self.window.profile.language_texts[30]+" \"{0}\"".format(self.select.get()), bg="red", command=self.delete_profile)
                self.deletion_button.grid(row=len(profiles_available), column=1)
                Button(self.frame2, text=self.window.profile.language_texts[27], bg="red", command=self.create_profile).grid(row=len(profiles_available)+1)
                Button(self.frame2, text=self.window.profile.language_texts[29], bg="red", command=self.upload_profile).grid(row=len(profiles_available)+1, column=1)
        def create_profile(self):
                os.remove("profile.txt")
                self.window.tk.destroy()
                main.main()
        def delete_profile(self):
                ask = messagebox.askyesno(self.window.profile.language_texts[20], self.window.profile.language_texts[31])
                if not ask:
                        return
                todelete = self.select.get()
                if todelete == self.name:
                        messagebox.showerror(self.window.profile.language_texts[20], self.window.profile.language_texts[33])
                        return
                os.remove("Profiles/"+todelete+"/data.json")
                os.rmdir("Profiles/"+todelete)
                messagebox.showinfo(self.window.profile.language_texts[20], self.window.profile.language_texts[32])
                self.window.tk.destroy()
                main.main()
        def create_manual_profile(self, name, data=None):
                os.mkdir("Profiles/"+name)
                with open("Profiles/"+name+"/data.json", "w") as f:
                        json.dump({"Trophies" : 0, "Brains" : 0, "Name" : name} if data is None else data, f) # Data RESET
                        f.close()
        def select_profile(self, name=None):
                with open("profile.txt", "w") as f:
                        f.write(self.select.get() if name is None else name)
                        f.close()
                n = self.select.get() if name is None else name
                messagebox.showinfo(self.window.profile.language_texts[20], self.window.profile.language_texts[28]+": \""+ n +"\"")
                self.window.tk.destroy()
                main.main()
        def download_profile(self):
                path = filedialog.asksaveasfilename(filetypes=[(".bin Bin File", "*.bin")], initialfile="profile_{0}".format(self.name), initialdir="Bin_downloads")
                if not path:
                        return
                f = open(path, "wb")
                pickle.dump(self.window.profile.data, f)
                messagebox.showinfo(self.window.profile.language_texts[20], self.window.profile.language_texts[24])
                f.close()
        def upload_profile(self):
                path = filedialog.askopenfilename(filetypes=[(".bin Bin File", "*.bin")], initialdir="Bin_downloads")
                if not path:
                        return
                f = open(path, "rb")
                d = pickle.load(f)
                if d["Name"] in os.listdir():
                        ask = messagebox.askyesno(self.window.profile.language_texts[20], self.window.profile.language_texts[34])
                        if not ask:
                                return
                        else:
                                os.remove(d["Name"]+"/data.json")
                                os.rmdir(d["Name"])
                self.create_manual_profile(d["Name"], d)
                self.select_profile(name=d["Name"])
                f.close()

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
                self.window.profile.load_languages()
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
                except Exception as e:
                        print(e)
                        messagebox.showerror("Error", "Internet Error, please verify your connection!")
                        shutil.rmtree("../.zombsAttack")
                        sys.exit()
                self.tk = Tk()
                self.tk.resizable(0, 0)
                self.tk.title("ZombsAttack Lobby - OrangoMangoGames")
                self.version_instance = version.Version(self)
                self.version_instance.get_data()
                self.check_update = self.version_instance.check()
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
                if self.check_update:
                        self.version_instance.show_gui()
                self.go = False
        def start(self, event):
                self.tk.quit()
                self.go = True
        def wait(self):
                while not self.go:
                        self.tk.update()
                        time.sleep(0.01)
