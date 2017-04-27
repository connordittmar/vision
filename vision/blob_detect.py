import cv2
import numpy as np

#Can be modified to detect different
class BlobDetector():

def __init__(self, minT, maxT, area):
    #Set up Blob Detector and Parameters (PARAMS NOT TESTED YET)
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = minT
    params.maxThreshold = maxT
    params.filterByArea = True
    params.minArea = area
    detector = cv2.SimpleBlobDetector_create(params)

def detectBlobs(im):
    keypoints = detector.detect(im)
    return keypoints

# blob = BlobDetector(50,250,150)
