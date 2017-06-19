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
            self.cam = urllib.urlopen('http://169.254.140.170/axis-cgi/jpg/image.cgi')
        except:
            print 'Axis IP Address Error'
            exit(0)

    def snapshot(self, save = True):
        bytes = ''
        bytes += self.cam.read()
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')

        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
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
        imgSetInfo = self.cam.getGigEImageSettingsInfo()
        imgSet = PyCapture2.GigEImageSettings()
        imgSet.offsetX = (2048-self.width)/2
        imgSet.offsetY = (2448-self.height)/2
        imgSet.height = self.height
        imgSet.width = self.width
        imgSet.pixelFormat = PyCapture2.PIXEL_FORMAT.RGB
        self.cam.setGigEImageSettings(imgSet)


    def snapshot(self):
        self.cam.startCapture()
        img = self.cam.retrieveBuffer()
        data = np.array(img.getData(),dtype=np.uint8)
        rgb = np.array(np.split(data,len(data)/3))
        rgb = rgb.reshape([self.height,self.width,3])
        bgr = rgb[...,[2,1,0]]
        self.cam.stopCapture()
        return bgr

    def disconnect(self):
        self.cam.disconnect()
'''
class Images(object):

    def __init__(self, img, timestamp=None):
        self.timestamp = timestamp
        self.img = img
        self.getTelemetryData(ip, port)
        self.calcualteExtrinsicMatrix()


    def calculateExtrinsicMatrix(self, lat, lon, alt, yaw, pitch, roll):
        self.Rt = np.eye(4)
        self._Rt[:3, :3] = angle2dcm(yaw, pitch, roll, input_units='rad').T
        self.lat =  lat
        self.lon = lon
        self.alt = alt
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll


    #Figure out payload format to decode mavlink messages****
    def getTelemetryData(self, ip, port):
        UDP_IP = ip
        UDP_PORT = port
        sock = socket.socket(socket.SOCK_DGRAM,sock)
        sock.bind((UDP_IP, UDP_PORT))
        data, ddr = sock.recvfrom(1024)
        self.msg = mav.decode(data)
'''
