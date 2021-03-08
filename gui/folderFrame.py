import tkinter as tk
from tkinter import filedialog, messagebox

from cbir import indexer
from gui import modals

class FolderFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.db = self.parent.db
        # self.loadingModal = modals.LoadingModal(self)

        labelFolder = tk.Label(self, text="Select Folder")
        labelFolder.grid(row=0, column=0, columnspan=2, sticky='ew')

        folderListboxScroll = tk.Scrollbar(self)
        folderListboxScroll.grid(row=1, column=1, rowspan=2, sticky='ns')

        self.folderListbox = tk.Listbox(self, yscrollcommand=folderListboxScroll.set)
        self.folderListbox.grid(row=1, column=0, rowspan=2, sticky='nsew')

        folderListboxScroll.config(command=self.folderListbox.yview)

        self.folderButtons = FolderButtonFrame(self)
        self.folderButtons.grid(row=1, column=2, rowspan=2, padx=(10,0), sticky='nsew')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.populate_folder_listbox()

    def populate_folder_listbox(self):
        if self.folderListbox.size() > 0:
            self.folderListbox.delete(0, 'end')

        folderpaths = self.parent.db.get_folder_index()

        if folderpaths:
            for f in folderpaths:
                self.folderListbox.insert('end', f[1])

    def get_folder(self):
        # paths = []
        # while True:
        #     path = filedialog.askdirectory(title='Choose Directories, Press Cancel to Stop')
        #     if path != '':
        #         paths.append(filedialog.askdirectory())
        #     else:
        #         break

        paths = filedialog.askdirectory()
        
        if indexer.indexer(paths):
            self.populate_folder_listbox()
        else:
            messagebox.showerror(title='Error', message='Folder doesn\'t contain image')
    
    def delete_folder(self):
        folderpaths = [self.folderListbox.get(i) for i in self.folderListbox.curselection()]

        if len(folderpaths) > 0 and messagebox.showwarning(title='Prompt', message='Delete selected folder(s)?') == 'ok':
            self.db.delete_folders_data(folderpaths)
            self.populate_folder_listbox()
        else:
            messagebox.showerror(title='Error', message='Please select folder(s) to delete')

class FolderButtonFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.folderDialogButton = tk.Button(self, text='Add', command=self.parent.get_folder)
        self.folderDialogButton.grid(row=0, column=0, sticky='ew')

        self.folderDeleteButton = tk.Button(self, text='Delete', command=self.parent.delete_folder)
        self.folderDeleteButton.grid(row=1, column=0, pady=(10,0), sticky='ew')

        folderSelectAllButton = tk.Button(self, text='Select All', command=lambda: self.parent.folderListbox.select_set(0, 'end'))
        folderSelectAllButton.grid(row=2, column=0, pady=(10,0), sticky='ew')

        folderDeselectAllButton = tk.Button(self, text='Deselect All', command=lambda: self.parent.folderListbox.select_clear(0, 'end'))
        folderDeselectAllButton.grid(row=3, column=0, pady=(10,0), sticky='ew')