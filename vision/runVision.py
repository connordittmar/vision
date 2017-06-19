import cv2
import numpy as np
import PyCapture2
from sys import exit
from Tkinter import *
from PIL import Image, ImageTk
import os
import time

from image_acquisition import *
from image_processing import BlobDetector, ImageClassifier

#Create function to process all images in a file
#Create multithreading image capturing in background
#Comment Code:(

class mainWindow(object):

    def __init__(self):
        self.vpath = "C:\\Users\\Suas Team\\Documents\\vision\\vision\\"
        self.root = Tk()
        self.root.geometry("1920x1080")

        MODES = [
            ("Blob Detection", 1),
            ("Classify Image", 2),
            ("Both", 3),
        ]
        self.v = StringVar()
        self.v.set("L")
        r = 10
        for text, mode in MODES:
            procMode = Radiobutton(self.root, text=text, variable=self.v, value=mode)
            procMode.grid(row=r, column=0)
            r += 1


        self.gigeLabel = Label(self.root, text='Not Connected', width=20, bg='red')
        self.gigeButton = Button(self.root, text="Init PointGrey Camera", width=20, command=self.initGige)
        self.gigeSnap = Button(self.root, text='PointGrey Snapshot', width=20, command=self.gigeSnapshot)
        self.quickGige = Button(self.root, text='Quick PointGrey Snap', width=20, command=self.qsGige)
        self.ipEntry = Entry(self.root, bg='red')
        self.ipEntry.insert(0,'169.254.140.170')
        self.axisButton = Button(self.root, text="Init Axis Camera", width=20, command=self.initAxis)
        self.axisSnap = Button(self.root, text='Axis Snapshot', width=20, command=self.axisSnapshot)
        self.quickAxis = Button(self.root, text='Quick Axis Snap', width=20, command=self.qsAxis)
        self.procButton = Button(self.root, text='Process Image', width=20, command=self.processImage)
        self.bdLabel = Label(self.root, text='Blob Detect Parameters', width=20)
        self.bdParams = Entry(self.root)
        self.bdParams.insert(0,'MinT,MaxT,area')
        self.qsLabel = Label(self.root, text='Quick Snap Number')
        self.qsSettings = Entry(self.root)


        self.gigeLabel.grid(row=0, column=0)
        self.gigeButton.grid(row=1, column=0)
        self.gigeSnap.grid(row=2, column=0)
        self.quickGige.grid(row=3, column=0)
        self.ipEntry.grid(row=5, column=0)
        self.axisButton.grid(row=6, column= 0)
        self.axisSnap.grid(row=7, column=0)
        self.quickAxis.grid(row=8, column=0)
        self.procButton.grid(row=9, column=0)
        #10-12 Radiobutton
        self.bdLabel.grid(row=13, column=0)
        self.bdParams.grid(row=14, column=0)
        self.qsLabel.grid(row=15, column=0)
        self.qsSettings.grid(row=16, column=0)


        self.imageCanvas = Canvas(width=1440, height=960)
        self.imageCanvas.grid(row=0, column=1, rowspan=100, columnspan=10)


        self.root.mainloop()

    def saveImage(self, p = "temp\\"):
        i = 1
        while os.path.exists("%s%simg%s.png"%(self.vpath,p,i)):
            i += 1
        cv2.imwrite('%simg%s.png'%(self.vpath,p,i), self.snap)

    def initGige(self):
        try:
            self.gige = gigeCam()
            self.gigeLabel.config(text='Connected', bg='green')
        except:
            self.gigeLabel.config(text="Not Connected", bg='red')

    def initAxis(self):
        try:
            self.axis = axisCam()
            self.ipEntry.delete(0,END)
            self.ipEntry.insert(0,'Connected')
            self.ipEntry.config(bg='green')
        except:
            self.ipEntry.delete(0,END)
            #self.ipEntry.insert(0,'Incorrect IP')

    def gigeSnapshot(self):
        self.snap = self.gige.snapshot()
        self.saveImage()
        self.updateImage()

    def axisSnapshot(self):
        self.snap = self.axis.snapshot()
        self.saveImage()
        self.updateImage()

    def qsGige(self):
        for i in (1,qsSettings.get()):
            self.gige.snapshot()
            time.sleep(.5)
            saveImage()

    def qsAxis(self):
        for i in (1,qsSettings.get()):
            self.axis.snapshot()
            time.sleep(.5)
            saveImage()


    def updateImage(self):
        self.img = Image.fromarray(self.snap[...,[2,1,0]], mode='RGB')
        self.photo = ImageTk.PhotoImage(image=self.img)
        self.imageCanvas.create_image(360, 240, image=self.photo)

    def updateProcessed(self):

        if procMode.get() == 1:
            self.tr = ImageTk.PhotoImage(Image.fromarray(self.imkp[...,[2,1,0]], mode='RGB'))
            self.bl = ImageTk.PhotoImage(Image.fromarray(self.blob[...,[2,1,0]]))
            self.br = ImageTk.PhotoImage(Image.fromarray(self.blob[...,[2,1,0]]))
        elif procMode.get() == 2:
            self.tr = ImageTk.PhotoImage(Image.fromarray(self.image.reduced, mode='RGB'))
            self.bl = ImageTk.PhotoImage(Image.fromarray(self.image.shape_bin))
            self.br = ImageTk.PhotoImage(Image.fromarray(self.image.letter_bin))
        else:
            self.tr = ImageTk.PhotoImage(Image.fromarray(self.self.blob[...,[2,1,0]], mode='RGB'))
            self.bl = ImageTk.PhotoImage(Image.fromarray(self.image.shape_bin))
            self.br = ImageTk.PhotoImage(Image.fromarray(self.image.letter_bin))


        self.imageCanvas.create_image(1080, 240, image=self.tr)
        self.imageCanvas.create_image(360, 720, image=self.bl)
        self.imageCanvas.create_image(1080, 720, image=self.br)

    def processImage(self):
        dparams = string.split(bdparams.get())
        if procMode.get()==1:
            self.detector = BlobDetector(dparams[0],dparams[2],dparams[2])
            self.kp = self.detector.detectBlobs(self.snap)
            self.blob = self.detector.isolateBlob(self.snap,self.kp)
            self.imgkp = detector.drawKeypoint(self.snap, self.kp)
        elif procMode.get()==2:
            self.image = ImageClassifier(self.snap,3)
        else:
            self.detector = BlobDetector(dparams[0],dparams[2],dparams[2])
            self.kp = detector.detectBlobs(self.snap)
            self.blob = detector.isolateBlob(self.snap,self.kp)
            self.imgkp = detector.drawKeypoint(self.snap, self.kp)
            self.image = ImageClassifier(self.blob,3)
        self.updateProcessed()

    def processFile(self, folder):
        dparams = string.split(bdparams.get())
        detector = BlobDetector = BlobDetector(dparams[0],dparams[1],dparams[2])
        i = 1
        while os.path.exists("C:\\Users\\SUAS Team\\Documents\\vision\\vision\\%s\\img%s"%(folder,i)):
            img = cv2.imread("C:\\Users\\SUAS Team\\Documents\\vision\\vision\\%s\\img%s"%(folder,i))
            kp = detector.detectBlobs(img)
            blob = detector.isolateBlob(img, kp)
            image = ImageClassifier(blob,3)
            cv2.imwrite("C:\\Users\\SUAS Team\\Documents\\vision\\vision\\%s\\reduced\\reduced%s"%(folder,i), image.reduced)
            cv2.imwrite("C:\\Users\\SUAS Team\\Documents\\vision\\vision\\%s\\shape\\shape%s"%(folder,i), image.shape_bin)
            cv2.imwrite("C:\\Users\\SUAS Team\\Documents\\vision\\vision\\%s\\letter\\letter%s"%(folder,i), image.letter_bin)
            cv2.imwrite("C:\\Users\\SUAS Team\\Documents\\vision\\vision\\%s\\keypoints\\keypoints%s"%(folder,i), image.shape_bin)

x = mainWindow()
