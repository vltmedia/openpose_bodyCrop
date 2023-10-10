import sys
import cv2
import os
import random
from sys import platform

# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname( os.path.dirname(os.path.realpath(__file__)))
print(dir_path)
try:
    # Change these variables to point to the correct folder (Release/x64 etc.)
    sys.path.append(dir_path + '/openpose/bin/python/openpose/Release')
    os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/openpose/bin/python/openpose/Release;' +  dir_path + '/openpose/bin;'
    import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e


targetPoints = {"points": [
     {"key":"head","point": [0,0,0], "index": 0},   
     {"key":"hip","point": [0,0,0], "index": 8},   
     {"key":"leftHand","point": [0,0,0], "index": 4},   
     {"key":"rightHand","point": [0,0,0], "index": 7}, 
     {"key":"leftShoulder","point": [0,0,0], "index": 2},   
     {"key":"rightShoulder","point": [0,0,0], "index": 5},  
     {"key":"leftHip","point": [0,0,0], "index": 9},   
     {"key":"rightHip","point": [0,0,0], "index": 12},   
     {"key":"leftFoot","point": [0,0,0], "index": 22},   
     {"key":"rightFoot","point": [0,0,0], "index": 19},   
    ]}

class OpenPoseBody:
    def __init__(self, image, modelFolder = "openpose/models", padding = [10,10,10,10], targetPoints = ["head","hip","leftHand","rightHand","leftShoulder","rightShoulder","leftHip","rightHip","leftFoot","rightFoot"]):
        self.image = image
        self.head = OpenPoseBodyPoint("head",self, index = 0)
        self.chest = OpenPoseBodyPoint("chest",self, index = 1)
        self.hip = OpenPoseBodyPoint("hip",self, index = 8)
        self.leftHand = OpenPoseBodyPoint("leftHand",self, index = 7)
        self.rightHand = OpenPoseBodyPoint("rightHand",self, index = 4)
        self.leftShoulder = OpenPoseBodyPoint("leftShoulder",self, index = 5)
        self.rightShoulder = OpenPoseBodyPoint("rightShoulder",self, index = 2)
        self.leftHip = OpenPoseBodyPoint("leftHip",self, index = 9)
        self.rightHip = OpenPoseBodyPoint("rightHip",self, index = 12)
        self.leftFoot = OpenPoseBodyPoint("leftFoot",self, index = 22)
        self.rightFoot = OpenPoseBodyPoint("rightFoot",self, index = 19)
        self.params = dict()
        self.params["model_folder"] = modelFolder
        self.boundingBox = [0,0,0,0]
        self.opWrapper = op.WrapperPython()
        self.outputImage = None
        self.padding = padding
        self.targetPoints = targetPoints

    def randomizePadding(self, left = [200, 300], top = [200, 300]):
        self.padding[0] = random.randrange(left[0], left[1],1)
        self.padding[1] = random.randrange(top[0], top[1],1)
        self.padding[2] = random.randrange(top[0], top[1],1)
        self.padding[3] = random.randrange(top[0], top[1],1)

    def processImage(self, imageToProcess):
        inpuImage = cv2.imread(imageToProcess)
        datum = op.Datum()
        datum.cvInputData = inpuImage
        self.opWrapper.configure(self.params)
        self.opWrapper.start()
        self.opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        self.outimage = datum.cvOutputData
        # cv2.imwrite("media/Lady_04_out1.jpg", inpuImage)
        # cv2.imwrite("media/Lady_04_out.jpg", self.outimage)
        self.points = datum.poseKeypoints[0]
        self.syncPoints()



    def syncPoints(self):
        self.head.syncPoint()
        self.chest.syncPoint()
        self.hip.syncPoint()
        self.leftHand.syncPoint()
        self.rightHand.syncPoint()
        self.leftShoulder.syncPoint()
        self.rightShoulder.syncPoint()
        self.leftHip.syncPoint()
        self.rightHip.syncPoint()
        self.leftFoot.syncPoint()
        self.rightFoot.syncPoint()
        self.calculateBoundingBox()
        
    def calculateBoundingBox(self):

        centerPoint = self.head.point
        # if "hip" in self.targetPoints:
        #     # set centerpoint to the center of self.head.point[1] and self.hip.point[1]
        #     centerPoint = [self.head.point[0], int((self.hip.point[1] + self.head.point[1])/2)]
        paddingX = self.padding[0]
        paddingY = self.padding[0]
        if "hip" in self.targetPoints:
            height = (self.hip.point[1] -  self.head.point[1] ) + self.padding[1] 
        if "chest" in self.targetPoints:
            height = (self.chest.point[1] -  self.head.point[1] ) + self.padding[1] 
            
        topPoint = self.head.point[1] - self.padding[1]
        bottomPoint = topPoint + height
        width = height

        self.top = [int(centerPoint[0]- ( width / 2)) , int(topPoint)]
        self.bottom = [int(centerPoint[0] + ( width / 2)), int(bottomPoint)]


        # self.top = [int(centerPoint[0] - paddingX), int(centerPoint[1] - paddingY)]
        # self.bottom = [int(centerPoint[0] + paddingX), int(centerPoint[1] + paddingY)]
        if self.top[0] < 0:
            self.top[0] = 0
        if self.bottom[0] > self.outimage.shape[0]:
            self.bottom[0] = self.outimage.shape[0]
        if self.top[1] > self.outimage.shape[1]:
            self.top[1] = self.outimage.shape[1]
        if self.bottom[1] < 0:
            self.bottom[1] = 0



        v = 0
    
    def drawBoundingBox(self):
        cv2.rectangle(self.outimage, self.top, self.bottom, (0, 255, 0), 2)
        # cv2.rectangle(self.outimage, (self.boundingBox[0], self.boundingBox[1]), (self.boundingBox[2], self.boundingBox[3]), (0, 255, 0), 2)

        
        

class OpenPoseBodyPoint:
    def __init__(self,name,openPoseBody, point = [0,0,0], index = 0):
        self.openPoseBody = openPoseBody
        self.name = name
        self.point = point
        self.index = index
    def syncPoint(self):
        self.point = self.openPoseBody.points[self.index]
        