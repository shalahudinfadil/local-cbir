import pickle

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import cv2

from cbir import hashing, indexer

class SearchFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, *kwargs)

        self.parent = parent
        self.db = self.parent.db

        self.searchButton = tk.Button(self, text='Search', command=self.search)
        self.searchButton.grid(row=0, column=0, sticky='ew', columnspan=2, pady=(0,10))

        searchResultTreeScroll = tk.Scrollbar(self)
        searchResultTreeScroll.grid(row=1,column=1, sticky='ns')

        self.searchResultTree = ttk.Treeview(self, yscrollcommand=searchResultTreeScroll.set)
        self.searchResultTree['columns'] = ('Rank', 'Path', 'Distance')

        self.searchResultTree.column('#0', width=0, stretch=tk.NO)
        self.searchResultTree.column('Rank', anchor=tk.CENTER, stretch=tk.NO)
        self.searchResultTree.column('Path')
        self.searchResultTree.column('Distance', anchor=tk.CENTER, stretch=tk.NO)

        self.searchResultTree.heading('#0', text='', anchor=tk.CENTER)
        self.searchResultTree.heading('Rank', text='Rank', anchor=tk.CENTER)
        self.searchResultTree.heading('Path', text='Path',)
        self.searchResultTree.heading('Distance', text='Distance', anchor=tk.CENTER)

        self.searchResultTree.grid(row=1, column=0, sticky='nsew')

        searchResultTreeScroll.config(command=self.searchResultTree.yview)

        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
    
    def tuplelist_to_dict(self, tupleList, key=0, removeKey=True):
        try:
            key = int(key)
        except ValueError:
            print('Key must be integer')

        if removeKey:
            tupleDict = { tl[key]:tl[:key] + tl[key+1:] for tl in tupleList }
        else:
            tupleDict = { tl[key]:tl for tl in tupleList }
        
        return tupleDict

    def key_zipper(self, treeRes, hashDB):    
        treeDict = self.tuplelist_to_dict(treeRes, 1)
        print(treeDict)
        hashDict = self.tuplelist_to_dict(hashDB, 1)
        print(hashDict)

        intersectKeys = [k for k in treeDict.keys() if k in hashDict.keys()]

        print(intersectKeys)

        return [(key, *treeDict[key], *hashDict[key]) for key in intersectKeys]
    
    def search(self):
        self.searchResultTree.delete(*self.searchResultTree.get_children())
        filepath = self.parent.imageFrame.entryImage.get()
        folderpaths = [self.parent.folderFrame.folderListbox.get(i) for i in self.parent.folderFrame.folderListbox.curselection()]

        if filepath != '' and len(folderpaths) > 0:
            imageFile = cv2.imread(filepath)
            imagehash = hashing.dhash(imageFile)
            imagehash = hashing.convert_hash(imagehash)

            treeResult = []

            result = self.db.get_folder_index(folderpaths)

            for r in result:
                with open(r[2], 'rb') as f:
                    tree = pickle.loads(f.read())
                    treeres = tree.get_all_in_range(imagehash, 10)
                    treeResult.extend(treeres)

            treeResult.sort(key=lambda t: t[0])
            treeResult = list(map(lambda t: (t[0], str(hashing.convert_hash(t[1]))), treeResult))
            hashResult = [str(hashing.convert_hash(t[1])) for t in treeResult]

            hashDB = self.db.get_hashes_images(hashResult)

            result = self.key_zipper(treeResult, hashDB)
            print(result)

            for i,h in enumerate(result):
                # image = self.parent.load_image(h[3])
                self.searchResultTree.insert(parent='', index=i, iid=i, values=(str(i+1), h[4], h[1]))

        else:
            messagebox.showerror(title='Error', message='Select an image and/or folder(s) first')