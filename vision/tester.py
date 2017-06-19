# tester for im_cam
import cv2
import urllib
import numpy as np
import PyCapture2
import pytesseract
from sys import exit
from PIL import Image

from image_acquisition import *
from image_processing import BlobDetector, ImageClassifier

def printImage(img):
    cv2.imshow('Image',img/255.0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


cam = gigeCam()
detector = BlobDetector(10, 255, 150)

snap = cam.snapshot()
#snap = cv2.imread('testshape.jpg')
image = ImageClassifier(snap,3)

print 'shape', image.hsvcolors[1], image.shape_color
print 'letter', image.hsvcolors[2], image.letter_color
image.saveImage()
cv2.imshow('red',image.reduced)
cv2.imshow('i',snap)
cv2.imshow('sharp', image.sharp)
cv2.imshow('s',image.shape_bin)
cv2.imshow('l',image.letter_bin)
cv2.waitKey(0)
cv2.destroyAllWindows()

'''
pic = Image.fromarray(np.uint8(image.letter_bin*255))
print type(pic)
letter = pytesseract.image_to_string(pic, lang = 'eng')
print letter
'''



'''
kp = detector.detectBlobs(snap)
detector.printKeypoint(snap,kp)
blob = detector.isolateBlob(snap, kp)
printImage(blob)
detector.getColor(blob)


lower = np.array([100,100,100], dtype=np.uint8)
upper = np.array([250,250,250], dtype=np.uint8)
mask = cv2.inRange(blob, lower, upper)


printImage(mask)
'''


#cam.disconnect()
