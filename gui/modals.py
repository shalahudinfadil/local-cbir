import tkinter as tk
import tkinter.ttk as ttk

class LoadingModal(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)

        self.progressBar = ttk.Progressbar(self,orient='horizontal', length=100, mode='indeterminate')
        self.progressBar.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.loadingLabel = tk.Label(self, text='Loading...')
        self.loadingLabel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.config(pady=10, padx=10)
    
    def show(self):
        self.grab_set()
        self.mainloop()
    
    def hide(self):
        self.destroy()