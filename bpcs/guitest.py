from tkinter import *
from tkinter import ttk
from tkinter import filedialog
# from PIL import ImageTk, Image
# import bcs
import os, shutil


import bpcs
from tkinter import *
from PIL import ImageTk,Image
import matplotlib.pyplot as plt
import cv2

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("CSC2004: BPCS")  # Set Name
        self.minsize(640, 400)  # Set Minimum size
        self.resizable(False, False)  # Dont let it resize

        # Upload Cover pic:
        self.CoverPicFrame = ttk.LabelFrame(self, text="Upload Cover Pic:")
        self.CoverPicFrame.grid(column=0, row=1, padx=30, pady=30)
        self.CoverPicbtton()

        # Upload Stego:
        self.StegoFrame = ttk.LabelFrame(self, text="Upload Stego:")
        self.StegoFrame.grid(column=9, row=1, padx=20, pady=20)
        self.Stegobtton()

        # Output:
        self.OutputFrame = ttk.LabelFrame(self, text="Output:")
        self.OutputFrame.grid(column=9, row=9, padx=20, pady=20)
        self.OutputTxtArea()
        self.Decryptbtton()

    # Upload Cover Pic Methods:
    def CoverPicbtton(self):
        self.CoverPicbutton = ttk.Button(self.CoverPicFrame, text="Upload Cover Pic", command=self.UploadCoverPic)
        self.CoverPicbutton.grid(column=1, row=1)

    def UploadCoverPic(self):
        self.filePath = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                                   filetype=(("jpeg", "*.jpg"), ("png", "*.png")))
        photo = PhotoImage(file=self.filePath)
        self.CoverPiclabel = ttk.Label(self.CoverPicFrame, text="")
        self.CoverPiclabel.grid(column=1, row=2)
        self.CoverPiclabel.configure(image=photo)

    # Stego Methods:
    def Stegobtton(self):
        self.StegoPicbutton = ttk.Button(self.StegoFrame, text="Upload Stego", command=self.UploadStego)
        self.StegoPicbutton.grid(column=4, row=1)

    def UploadStego(self):
        # include more types here:
        self.StegofilePath = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                                   filetype=(("jpeg", "*.jpg"), ("png", "*.png"), ("txt", "*.txt")))
        self.Stegolabel = ttk.Label(self.StegoFrame, text="")
        self.Stegolabel.grid(column=4, row=2)
        self.Stegolabel.configure(text=self.StegofilePath)

    # output text Area:
    def OutputTxtArea(self):
        self.Outputlabel = ttk.Label(self.OutputFrame, text="testing")
        self.Outputlabel.grid(column=10, row=11)
        # use this to set the output:
        # self.label.configure(text=...)
        self.Outputlabel.configure(text="Output text here")

    def Decryptbtton(self):
        self.Startbutton = ttk.Button(self.OutputFrame, text="Start Decrypt", command=self.StartDecrypt)
        self.Startbutton.grid(column=10, row=10)

    def StartDecrypt(self):
        alpha = 0.45
        vslfile = 'C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/vessel.png'
        msgfile = 'C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/message.txt' # can be any type of file
        encfile = 'C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/encoded.png'
        msgfile_decoded = 'C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/tmp.txt'

        #bpcs.capacity(vslfile, alpha) # check max size of message you can embed in vslfile
        bpcs.encode(vslfile, msgfile, encfile, alpha) # embed msgfile in vslfile, write to encfile
        bpcs.decode(encfile, msgfile_decoded, alpha) # recover message from encfile 

        path = "C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/"

        imgpath1 = path + "vessel.png"
        imgpath2 = path + "encoded.png"

        img1 = cv2.imread(imgpath1,1)
        img2 = cv2.imread(imgpath2,2)

        img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

        titles = ['Cover Image', 'Stego Object']
        images = [img1, img2]

        for i in range(2):
            plt.subplot(1,2,i+1)
            plt.imshow(images[i])
            plt.title(titles[i])
            plt.xticks([])
            plt.yticks([])
        plt.show()


if name == '__main__':
    root = Root()
    root.mainloop()