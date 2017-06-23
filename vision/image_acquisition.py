import cv2
import urllib
import numpy as np
import scipy
import PyCapture2
import socket
from sys import exit
#from pymavlink import mavlink10 as mavlink

class axisCam(object):

    def __init__(self, ip='169.254.140.171'):
        try:
            #self.cam = urllib.urlopen('http://%s/axis-cgi/jpg/image.cgi'%ip)
            self.cam = urllib.urlopen('http://169.254.171.248/axis-cgi/jpg/image.cgi')
            self.bytes = ''
        except:
            print 'Axis IP Address Error'
            exit(0)

    def snapshot(self, save = True):
        self.bytes = ''  #Image Buffer
        self.bytes += self.cam.read()  #Update buffer
        #Locate full image in buffer
        a = self.bytes.find('\xff\xd8')
        b = self.bytes.find('\xff\xd9')

        #Format image as numpy array
        if a!=-1 and b!=-1:
            jpg = self.bytes[a:b+2]
            #bytes= bytes[b+2:]
            img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
        return img

class gigeCam(object):

    def __init__(self, width=720, height=480):

        self.width = width
        self.height = height

        #Connect to Camera
        bus = PyCapture2.BusManager()
        camInfo = bus.discoverGigECameras()
        self.cam = PyCapture2.GigECamera()
        uID = bus.getCameraFromIndex(0)
        self.cam.connect(uID)

        #Set Up Camera Parameters
        #imgSetInfo = self.cam.getGigEImageSettingsInfo()
        imgSet = PyCapture2.GigEImageSettings() #Get Camera Settings
        imgSet.offsetX = (2048-self.width)/2    #Center Image
        imgSet.offsetY = (2448-self.height)/2   #Center Image
        imgSet.height = self.height
        imgSet.width = self.width
        imgSet.pixelFormat = PyCapture2.PIXEL_FORMAT.RGB
        self.cam.setGigEImageSettings(imgSet)


    def snapshot(self):
        self.cam.startCapture()
        img = self.cam.retrieveBuffer() #grab Image from buffer
        data = np.array(img.getData(),dtype=np.uint8)   #Format image as numpy array
        rgb = np.array(np.split(data,len(data)/3)) #Split numpy array into RGB channels
        rgb = rgb.reshape([self.height,self.width,3]) #Shape RGB channels into proper image array
        bgr = rgb[...,[2,1,0]]  #Convert rgb to bgr
        self.cam.stopCapture()
        return bgr

    def getBuffer(self):
        return self.cam.retrieveBuffer()

    def startStream(self):
        self.cam.startCapture()

    def stopStream(self):
        self.cam.stopCapture()

    def disconnect(self):
        self.cam.disconnect()
