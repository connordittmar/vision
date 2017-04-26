import cv2
import numpy as np

def initBlobDetector():
    #Set up Blob Detector and Parameters
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 50
    params.maxThreshold = 150
    params.filterByArea = True
    params.minArea = 150
    #params.filterByColor = false
    detector = cv2.SimpleBlobDetector_create(params)
    return detector

def detectBlobs(im, detector):
    keypoints = detector.detect(im)
    return keypoints
