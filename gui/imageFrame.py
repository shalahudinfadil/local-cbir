import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        imageFolder = tk.Label(self, text="Select Image")
        imageFolder.grid(row=0, column=0, columnspan=2, sticky='ew')
 
        self.imagePlaceholder = self.parent.load_image('./cbir/placeholder.png')
        self.entryImagePreview = tk.Label(self, image=self.imagePlaceholder)
        self.entryImagePreview.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=10)

        self.entryImage = tk.Entry(self)
        self.entryImage.grid(row=2, column=0, sticky='nsew', padx=(0,10))

        self.imageDialogButton = tk.Button(self, text='Browse', command=self.get_image)
        self.imageDialogButton.grid(row=2, column=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def get_image(self):
        filepath = filedialog.askopenfilename(filetypes=[('Image File', ('.png', '.jpg','.jpeg')),])
        self.entryImage.delete(0,'end')

        if filepath is not None:
            self.entryImage.insert(0, filepath)

            imageFile = self.parent.load_image(filepath)

            self.entryImagePreview.configure(image=imageFile)
            self.entryImagePreview.photo = imageFile