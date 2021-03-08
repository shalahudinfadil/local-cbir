import tkinter as tk

class Menu(tk.Menu):
    def __init__(self, parent, *args, **kwargs):
        tk.Menu.__init__(self, parent, *args, **kwargs)

        settingMenu = tk.Menu(self, tearoff=0)