import tkinter as tk
from tkinter import Image, filedialog, messagebox
import tkinter.ttk as ttk
import pickle

from PIL import Image, ImageTk
import cv2

from cbir import indexer, hashing
from db import db
from gui import imageFrame, folderFrame, searchFrame

class MainFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.db = db.DB()
        self.initFrames()
    
    def initFrames(self):
        self.imageFrame = imageFrame.ImageFrame(self)
        self.imageFrame.grid(row=0,column=0, sticky='nsew')

        separator = ttk.Separator(self, orient='vertical')
        separator.grid(row=0, column=1, sticky='ns', padx=10)

        self.folderFrame = folderFrame.FolderFrame(self)
        self.folderFrame.grid(row=0,column=2, sticky='nsew')

        self.folderFrame.populate_folder_listbox()

        searchSeparator = ttk.Separator(self, orient='horizontal')
        searchSeparator.grid(row=1, column=0, columnspan=3, sticky='ew', pady=10)

        self.searchFrame = searchFrame.SearchFrame(self)
        self.searchFrame.grid(row=2, column=0, columnspan=3, sticky='ew')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)

    def load_image(self, imagepath):
        imageFile = Image.open(imagepath)
        imageFile.thumbnail((500,500), Image.ANTIALIAS)
        imageFile = ImageTk.PhotoImage(imageFile)
        
        return imageFile

    def get_folder(self):
        path = filedialog.askdirectory()
        
        indexer.indexer(path)
        self.populate_folder_listbox()
    
    def populate_folder_listbox(self):
        if self.folderListbox.size() > 0:
            self.folderListbox.delete(0, 'end')

        folderpaths = self.db.get_folder_index()

        if folderpaths:
            for f in folderpaths:
                self.folderListbox.insert('end', f[1])

    def search(self):
        filepath = self.imageFrame.entryImage.get()
        folderpaths = [self.folderListbox.get(i) for i in self.folderListbox.curselection()]

        if filepath != '' and len(folderpaths) > 0:
            imageFile = cv2.imread(filepath)
            imagehash = hashing.dhash(imageFile)
            imagehash = hashing.convert_hash(imagehash)

            hashResult = []

            result = self.db.get_folder_index(folderpaths)
            print(result)
            for r in result:
                with open(r[2], 'rb') as f:
                    tree = pickle.loads(f.read())
                    treeres = tree.get_n_nearest_neighbors(imagehash, 10)
                    for t in treeres:
                        print(t[1])
                        hashResult.append(str(t[1]))
            print(hashResult)
            hashDB = self.db.get_hashes_images(hashResult)
            print(hashDB)

                    
        else:
            messagebox.showerror(title='Error', message='Please select an image and folder(s) first')

    