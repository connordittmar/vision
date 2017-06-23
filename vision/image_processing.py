import cv2          #OpenCV 2.7
import numpy as np
import scipy
import os

#Can be modified to detect different
class BlobDetector(object):
    #Create Custom Blob Detector in Future

    def __init__(self, minT, maxT, area):
        #Set up Blob Detector and Parameters (PARAMS NOT TESTED YET)
        params = cv2.SimpleBlobDetector_Params()
        params.minThreshold = minT
        params.maxThreshold = maxT
        params.filterByArea = True
        params.minArea = area
        self.detector = cv2.SimpleBlobDetector_create(params)

    def detectBlobs(self, img):
        #Retruns Array of keypoints of blobs in image
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        keypoints = self.detector.detect(img) #Find keypoits of blobs in image
        return keypoints

    def drawKeypoint(self,img,kp):
        #Print Image with marked keypoints
        imgkp = cv2.drawKeypoints(img, kp, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        return imgkp

    def isolateBlob(self,img,kp):
        #Return Cropped Image of Largest blob
        if len(kp) != 0: #Pick largest blob (Just for testing)
            maxkp = 0
            maxsize = 0
            for i in kp:
                if i.size > maxsize:
                    maxkp = i
                    maxsize = i.size

            #Crom image based on blob size
            shift = int(maxkp.size/1.5) #Set crop size to be slightly larger than blob
            startx = int(maxkp.pt[0]-shift) #Set starting point of crop
            starty = int(maxkp.pt[1]-shift)
            return img[starty:starty+shift*2,startx:startx+shift*2]
        else:
            #If no blobs, return imput image
            print 'No Blob'
            return img



class ImageClassifier(object):

    def __init__(self, img, k=3):

        self.img = img
        self.k = k

        self.sharpenImage()
        self.reduceColorspace()
        self.findColors()
        self.isolateShapes()


    def reduceColorspace(self):
        #Reduces the Image to 3 colors using kmeans clustering
        z = self.sharp.reshape((-1,3))
        z = np.float32(z)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0) #Criteria for kmeans clustering
        ret,label,center=cv2.kmeans(z,self.k,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)    #Apply kmeans clustering
        #Create image from clusters
        center = np.uint8(center)
        res = center[label.flatten()]
        self.reduced = res.reshape((self.img.shape))

    def sharpenImage(self):
        #Sharpen the image for more defined kmeans
        kernel = np.zeros((9,9), np.float32)
        kernel[4,4] = 2.0
        boxFilter = np.ones((9,9), np.float32)/70.0  #81.0
        kernel = kernel - boxFilter
        self.sharp = cv2.filter2D(self.img, -1, kernel)


    def hsvToName(self, triplet):
        #Get hsv value from triplet for easier referencing
        h = triplet[0]
        s = triplet[1]
        v = triplet[2]

        #Use visually picked hsv values for colors for 10 competition colors
        if v<50:
            return 'black'
        elif v>210 and s<26:
            return 'white'
        elif h>190 and h<230 and s>86:
            return 'purple'
        elif h>135 and h<188 and s>60 and v>64 and v<155:
            return 'purple'
        elif h<=5 or h>175:
            return 'red'
        elif h>5 and h<=25:
            if v>28 and v<212 and s<38:
                return 'brown'
            else:
                return 'orange'
        elif h>25 and h<=50:
            return 'yellow'
        elif h>50 and h<=100:
            return 'green'
        else:
            return 'blue'



    def findColors(self):
        #Find all colors in an image as RGB, BGR, HSV, and name
        im = self.reduced[...,[2,1,0]] #Turn reduced to rgb
        self.hsv = cv2.cvtColor(self.reduced,cv2.COLOR_BGR2HSV) #Create hsv image
        #List of colors in image in different color spaces
        self.rgbcolors=[]
        self.bgrcolors=[]
        self.hsvcolors=[]
        #Loop through pixels in image to find all of colors in reduced image
        for i in xrange(0,im.shape[0]):
            for j in xrange(0,im.shape[1]):
                l = list(im[i,j])   #Convert numpy array to list
                try:
                    self.rgbcolors.index(l) #Check if color has been counted
                except:
                    #If color hasnt been recorded, add it to the color space lists
                    self.rgbcolors.append(l)
                    self.bgrcolors.append(l[::-1])
                    self.hsvcolors.append(list(self.hsv[i,j]))

                #Break loops once all color shave been found to avoid going through whole image
                if len(self.rgbcolors) == self.k:
                    break
            else:
                continue
            break

        #Find list of color names
        self.colors = []
        for i in range(0,len(self.hsvcolors)):
            colorName = self.hsvToName(self.hsvcolors[i]) #Plug in HSV triplet to get name
            self.colors.append(colorName)
        self.shape_color =  self.colors[1]  #Second color should be shape based on loop
        self.letter_color = self.colors[2]  #Third color in list should be letter based on loop

    def isolateShapes(self):
        #Create Binaies of the shape and letter from a 3 color reduction
        #Shape binary is the inverse of the background binary to avoid having the latter in the middle
        lower = np.array(self.bgrcolors[0]) #Set values for binarization
        upper = np.array(self.bgrcolors[0])
        self.shape_bin = np.invert(cv2.inRange(self.reduced, lower, upper))
        lower = np.array(self.bgrcolors[2])
        upper = np.array(self.bgrcolors[2])
        self.letter_bin = cv2.inRange(self.reduced, lower, upper)
