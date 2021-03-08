import tkinter as tk

from cbir import hashing, indexer
from gui import mainFrame

class Root(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        mainFrameComp = mainFrame.MainFrame(self)
        mainFrameComp.grid(row=0,column=0, sticky='nsew', padx=10, pady=10)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
    
    def run(self):
        self.title('Local CBIR')
        self.geometry('1366x768')
        self.mainloop()

if __name__ == '__main__':
    
    Root().run()