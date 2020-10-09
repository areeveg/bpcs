from tkinter import *
from tkinter import ttk
from tkinter import filedialog
# from PIL import ImageTk, Image
# import bcs
import os, shutil


import os, sys
from utils import rgb_to_binary, add_leading_zeros


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


        # Upload Payload Image:
        self.imgFrame = ttk.LabelFrame(self, text="Upload Stego:")
        self.imgFrame.grid(column=5, row=1, padx=20, pady=20)
        self.imgbtton()

        # Output:
        self.OutputFrame = ttk.LabelFrame(self, text="Output:")
        self.OutputFrame.grid(column=9, row=9, padx=20, pady=20)
        self.OutputTxtArea()
        self.Decryptbtton()

        # Outputimg:
        self.OutputimgFrame = ttk.LabelFrame(self, text="Output img:")
        self.OutputimgFrame.grid(column=5, row=11, padx=20, pady=20)
        self.Encryptimagebtton()
    
     # Stego Methods:
    def imgbtton(self):
        self.imgPicbutton = ttk.Button(self.imgFrame, text="Upload Imgage", command=self.Uploadimg)
        self.imgPicbutton.grid(column=4, row=1)
    
    def Uploadimg(self):
        # include more types here:
        self.imgfilePath = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                                   filetype=(("jpeg", "*.jpg"), ("png", "*.png"), ("txt", "*.txt")))
        self.imglabel = ttk.Label(self.imgFrame, text="")
        self.imglabel.grid(column=4, row=2)
        self.imglabel.configure(text=self.imgfilePath)

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

    def Encryptimagebtton(self):
        self.imgbutton = ttk.Button(self.OutputimgFrame, text="Start Decrypt", command=self.StartEncrypt)
        self.imgbutton.grid(column=0, row=15)
#------------------------------------------------------------------------------------------------------------------------------------
    def StartEncrypt(self):
        
        path = "C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/"
        output_path = 'C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/encoded_image.png'
        img_visible_path = path + "vessel.png"
        img_hidden_path = path + "payload.png"
        img_visible = Image.open(img_visible_path)
        img_hidden = Image.open(img_hidden_path)
        encoded_image = self.encode(img_visible, img_hidden)
        encoded_image.save(output_path)

        #show images side by side###########################################################
        imgpath1 = path + "vessel.png"
        imgpath2 = path + "encoded_image.png"
        img1 = cv2.imread(imgpath1,1)
        img2 = cv2.imread(imgpath2,1)

        img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
        img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)

        titles = ['Cover Image', 'encoded Image']
        images = [img1, img2]

        for i in range(2):
            plt.subplot(1,2,i+1)
            plt.imshow(images[i])
            plt.title(titles[i])
            plt.xticks([])
            plt.yticks([])
        plt.show()

    def get_binary_pixel_values(self, img, width, height):
        hidden_image_pixels = ''
        for col in range(width):
            for row in range(height):
                pixel = img[col, row]
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]
                r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
                hidden_image_pixels += r_binary + g_binary + b_binary
        return hidden_image_pixels

    def change_binary_values(self,img_visible, hidden_image_pixels, width_visible, height_visible, width_hidden, height_hidden):
        idx = 0
        for col in range(width_visible):
            for row in range(height_visible):
                if row == 0 and col == 0:
                    width_hidden_binary = add_leading_zeros(bin(width_hidden)[2:], 12)
                    height_hidden_binary = add_leading_zeros(bin(height_hidden)[2:], 12)
                    w_h_binary = width_hidden_binary + height_hidden_binary
                    img_visible[col, row] = (int(w_h_binary[0:8], 2), int(w_h_binary[8:16], 2), int(w_h_binary[16:24], 2))
                    continue
                r, g, b = img_visible[col, row]
                r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
                r_binary = r_binary[0:4] + hidden_image_pixels[idx:idx+4]
                g_binary = g_binary[0:4] + hidden_image_pixels[idx+4:idx+8]
                b_binary = b_binary[0:4] + hidden_image_pixels[idx+8:idx+12]
                idx += 12
                img_visible[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
                if idx >= len(hidden_image_pixels):
                    return img_visible
        # can never be reached, but let's return the image anyway
        return img_visible

    def encode(self,img_visible, img_hidden):
        encoded_image = img_visible.load()
        img_hidden_copy = img_hidden.load()
        width_visible, height_visible = img_visible.size
        width_hidden, height_hidden = img_hidden.size
        hidden_image_pixels = self.get_binary_pixel_values(img_hidden_copy, width_hidden, height_hidden)
        encoded_image = self.change_binary_values(encoded_image, hidden_image_pixels, width_visible, height_visible, width_hidden, height_hidden)
        return img_visible
    

    def StartDecrypt(self):
        alpha = 0.45
        vslfile = 'C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/vessel.png'
        msgfile = 'C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/message.txt' # can be any type of file
        encfile = 'C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/encoded.png'
        msgfile_decoded = 'C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/tmp.txt'

        #bpcs.capacity(vslfile, alpha) # check max size of message you can embed in vslfile
        #img = cv2.imread('C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/payload.png')
        #img3 = cv2.imread('C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/vessel.png')
        #vslfile = cv2.imencode('.png', img3)[1].tobytes()
        #type(vslfile)
        #msgfile = cv2.imencode('.png', img)[1].tobytes()
        #type(msgfile)
        bpcs.encode(vslfile, msgfile, encfile, alpha) # embed msgfile in vslfile, write to encfile
        bpcs.decode(encfile, msgfile_decoded, alpha) # recover message from encfile 

        path = "C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/"

        imgpath1 = path + "vessel.png"
        imgpath2 = path + "encoded.png"

        img1 = cv2.imread(imgpath1,1)
        img2 = cv2.imread(imgpath2,1)

        img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
        img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)

        titles = ['Cover Image', 'Stego Object']
        images = [img1, img2]

        for i in range(2):
            plt.subplot(1,2,i+1)
            plt.imshow(images[i])
            plt.title(titles[i])
            plt.xticks([])
            plt.yticks([])
        plt.show()


if __name__ == '__main__':
    root = Root()
    root.mainloop()