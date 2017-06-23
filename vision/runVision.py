import cv2
import numpy as np
import PyCapture2
from sys import exit
from Tkinter import *
from PIL import Image, ImageTk
import os
import time
import threading

from image_acquisition import *
from image_processing import BlobDetector, ImageClassifier

#Create function to process all images in a file
#Create multithreading image capturing in background
#Comment Code:(

class mainWindow(object):

    def __init__(self):
        self.vpath = "C:\\Users\\Suas Team\\Documents\\vision\\vision\\" #path for the vision folder
        #Create GUI frame
        self.root = Tk()
        self.root.geometry("1920x1080")

        #Create Radiobutton to pick image processing method
        MODES = [
            ("Blob Detection", 1),
            ("Classify Image", 2),
            ("Both", 3),
        ]
        self.v = StringVar()
        self.v.set("L")
        r = 11 #Starting Grid position of buttons
        for text, mode in MODES:    #Place down Radio Buttons
            procMode = Radiobutton(self.root, text=text, variable=self.v, value=mode)
            procMode.grid(row=r, column=0)
            r += 1

        #Create Buttons/Text Box/etc. for GUI
        self.gigeLabel = Label(self.root, text='Not Connected', width=20, bg='red') #Label PointGrey Section
        self.gigeButton = Button(self.root, text="Init PointGrey Camera", width=20, command=self.initGige)  #Button to initialize Pointgrey Camera
        self.gigeSnap = Button(self.root, text='PointGrey Snapshot', width=20, command=self.gigeSnapshot)   #Button to take PointGrey Snapshot
        self.quickGige = Button(self.root, text='Quick PointGrey Snap', width=20, command=self.qsGige)  #Button to take series of quick snapshots with Pointgrey
        self.gigeStreamButton = Button(self.root, text='Stream PointGrey Video', width=20, command=self.startGigeStream)
        self.ipEntry = Entry(self.root, bg='red')   #Entry Space for IP address of Axis Camera
        self.ipEntry.insert(0,'169.254.140.170')    #Default Entry for Axis IP
        self.axisButton = Button(self.root, text="Init Axis Camera", width=20, command=self.initAxis)   #Button to initialize Axis Camera
        self.axisSnap = Button(self.root, text='Axis Snapshot', width=20, command=self.axisSnapshot)    #Button to take Axis snapshot
        self.quickAxis = Button(self.root, text='Quick Axis Snap', width=20, command=self.qsAxis)       #Button to take series of quick snapshots iwth Axis
        self.axisStreamButton = Button(self.root, text='Stream Axis Video', width=20, command=self.startAxisStream) #Button to start Axis video stream
        self.procButton = Button(self.root, text='Process Image', width=20, command=self.processImage)  #Button to process previous image
        self.bdLabel = Label(self.root, text='Blob Detect Parameters', width=20)    #Label For Blob Detection Entry Box
        self.bdParams = Entry(self.root)       #Entry Space for blob detection Parameters
        self.bdParams.insert(0,'MinT,MaxT,area') #Tells user how to input entry into blob detection parameters
        self.qsLabel = Label(self.root, text='Quick Snap Number') #Label FOr quick snap settings
        self.qsSettings = Entry(self.root)  #Entry for number of snapshots to take in the quick snaps

        #Place objects onto GUI using grid format
        self.gigeLabel.grid(row=0, column=0)
        self.gigeButton.grid(row=1, column=0)
        self.gigeSnap.grid(row=2, column=0)
        self.quickGige.grid(row=3, column=0)
        self.gigeStreamButton.grid(row=4, column=0)
        self.ipEntry.grid(row=5, column=0)
        self.axisButton.grid(row=6, column= 0)
        self.axisSnap.grid(row=7, column=0)
        self.quickAxis.grid(row=8, column=0)
        self.axisStreamButton.grid(row=9, column=0)
        self.procButton.grid(row=10, column=0)
        #11-13 Radiobutton
        self.bdLabel.grid(row=14, column=0)
        self.bdParams.grid(row=15, column=0)
        self.qsLabel.grid(row=16, column=0)
        self.qsSettings.grid(row=17, column=0)

        #Create Camvas to Put images on
        self.imageCanvas = Canvas(width=1820, height=960)
        #Plac e canvas. Large Rowspan to prevent wide rowson other labels
        self.imageCanvas.grid(row=0, column=1, rowspan=100, columnspan=10)

        #Run Gui
        self.root.mainloop()

    def saveImage(self, p = "temp"):
        #Save numbered to specified file within vision
        #If folder doesn't exist, create folder
        if not os.path.exists("%s%s"%(self.vpath,p)):
            os.makedirs("%s%s"%(self.vpath,p))
        i = 1
        #Increment image file number
        while os.path.exists("%s%s\\img%s.png"%(self.vpath,p,i)):
            i += 1
        cv2.imwrite('%s%s\\img%s.png'%(self.vpath,p,i), self.snap)

    def initGige(self):
        #Try to Connect to PointGrey Camera
        try:
            self.gige = gigeCam()
            self.gigeLabel.config(text='Connected', bg='green')
        except:
            self.gigeLabel.config(text="Not Connected", bg='red')

    def initAxis(self):
        #Try to connect to Axis Camera
        try:
            self.axis = axisCam()
            self.ipEntry.delete(0,END)
            self.ipEntry.insert(0,'Connected')
            self.ipEntry.config(bg='green')
        except:
            self.ipEntry.delete(0,END)
            #self.ipEntry.insert(0,'Incorrect IP')

    def gigeSnapshot(self):
        #Take and save snapshot from PointGrey Camera
        self.snap = self.gige.snapshot()
        self.saveImage()
        self.updateImage() #Show snapshot on canvas

    def axisSnapshot(self):
        #Take and save snapshot from Axis Wide Angle camera
        self.snap = self.axis.snapshot()
        self.saveImage()
        self.updateImage() #Show snapshot on canvas

    def qsGige(self):
        #Quicksnap Specified number of snaps from PointGrey
        for i in (1,qsSettings.get()):
            self.gige.snapshot()
            time.sleep(.5) #Time between Snaoshots
            saveImage()

    def qsAxis(self):
        #Quicksnap specified number of snaps for Axis
        for i in (1,qsSettings.get()):
            self.axis.snapshot()
            time.sleep(.5) #Time between snaposhots
            saveImage()

    def startAxisStream(self):
        #Create thread for video stream
        axisThread = threading.Thread(target=self.axisStream)
        #Start stream thread
        axisThread.start()

    def startGigeStream(self):
        gigeThread = threading.Thread(target=self.gigeStream)
        gigeThread.start()

    def axisStream(self):
        #Stream Video From Axis Camera
        stream = urllib.urlopen('http://169.254.171.248/mjpg/video.mjpg') #Connect to camera mjpg stream
        bytes = ''  #Create buffer for stream
        while True:
            bytes += stream.read(1024) #Update buffer
            a = bytes.find('\xff\xd8') #FInd Previous Image in buffer
            b = bytes.find('\xff\xd9')
            #Format image to place on Canvas
            if a!=-1 and b!=-1:
                jpg = bytes[a:b+2]
                bytes= bytes[b+2:]
                i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
                tki = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(i, cv2.COLOR_BGR2RGB)))
                self.imageCanvas.create_image(360, 240, image=tki)
            if cv2.waitKey(1) == 32:
                break


    def gigeStream(self):
        self.gige.startStream()
        while True:
            img = self.gige.getBuffer()
            data = np.array(img.getData(), dtype=np.uint8)
            rgb = np.array(np.split(data,len(data)/3))
            rgb = rgb.reshape([self.gige.height,self.gige.width,3])
            tki = ImageTk.PhotoImage(Image.fromarray(rgb))
            self.imageCanvas.create_image(1380,240, image=tki)
            if cv2.waitKey(1) == 27:
                self.gige.stopStream()
                break

    def updateImage(self):
        #Put most recent snap into top left picture of canvas(Requires Image format changes)
        self.img = Image.fromarray(self.snap[...,[2,1,0]], mode='RGB') #PIL Image
        self.photo = ImageTk.PhotoImage(image=self.img) #ImageTK Image
        self.imageCanvas.create_image(360, 240, image=self.photo)

    def updateProcessed(self):

        #Place selected images into different image locations on canvas
        #tr=top-right, bl=bottom-left, etc.
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

        self.imageCanvas.create_image(1080, 240, image=self.tr) #Place in top right
        self.imageCanvas.create_image(360, 720, image=self.bl)  #Place in bottom left
        self.imageCanvas.create_image(1080, 720, image=self.br) #Place in bottom right


    def processImage(self):
        #Blob Detection and/or shape/letter classification in singe image (Look at image_processing.py for detailson image processing)
        dparams = string.split(bdparams.get())  #Read Entry for blod detection parameters
        #Process Image based on choice in Radiobutton
        if procMode.get()==1:
            self.detector = BlobDetector(dparams[0],dparams[2],dparams[2]) #Create blob detector
            self.kp = self.detector.detectBlobs(self.snap) #Find blob keypoints
            self.blob = self.detector.isolateBlob(self.snap,self.kp) #Crop out a keypoint
            self.imgkp = detector.drawKeypoint(self.snap, self.kp)  #Create image with circled keypoints
        elif procMode.get()==2:
            self.image = ImageClassifier(self.snap,3) #Classify Images
        else:
            self.detector = BlobDetector(dparams[0],dparams[2],dparams[2])
            self.kp = detector.detectBlobs(self.snap)
            self.blob = detector.isolateBlob(self.snap,self.kp)
            self.imgkp = detector.drawKeypoint(self.snap, self.kp)
            self.image = ImageClassifier(self.blob,3)
        self.updateProcessed()  #Place Images on canvas


    def processFile(self, folder):
        #Process all images in specified file
        dparams = string.split(bdparams.get())
        detector = BlobDetector = BlobDetector(dparams[0],dparams[1],dparams[2])
        i = 1
        #Loop through Images im file
        while os.path.exists("%s%s\\img%s"%(self.vpath,folder,i)):
            img = cv2.imread("5s%s\\img%s"%(self.vpath,folder,i))
            #Process selected image
            kp = detector.detectBlobs(img)
            blob = detector.isolateBlob(img, kp)
            image = ImageClassifier(blob,3)
            #Save Processed Images to folders
            cv2.imwrite("%s%s\\reduced\\reduced%s"%(self.vpath,folder,i), image.reduced)
            cv2.imwrite("%s%s\\shape\\shape%s"%(self.vpath,folder,i), image.shape_bin)
            cv2.imwrite("%s%s\\letter\\letter%s"%(self.vpath,folder,i), image.letter_bin)
            cv2.imwrite("%s%s\\keypoints\\keypoints%s"%(self.vpath,folder,i), image.shape_bin)

#Run GUI
x = mainWindow()
