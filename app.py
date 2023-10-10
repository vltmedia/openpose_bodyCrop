# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
import base64
import json
from io import BytesIO
from sys import platform
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from uaiPose.openPoseBody import OpenPoseBody


def RunProcess(req):
    openPoseBody = OpenPoseBody( req['input'], "openpose/models", targetPoints=req["targetPoints"])
    # openPoseBody = OpenPoseBody( 'media/Lady_04.jpg', "openpose/models", targetPoints=["head", "hip"])
    openPoseBody.randomizePadding(  left = req['leftPadding'], top = req['topPadding'])
    openPoseBody.processImage(openPoseBody.image)
    openPoseBody.drawBoundingBox()
    type_ = "image/jpeg"
    if "png" in openPoseBody.outimage:
        type_ = "image/png"
    outData = {"media":[{"media": base64.b64encode(openPoseBody.outimage).decode('utf-8'), "type": type_}]}
    return json.dumps(outData, indent=4)
    
    # # cv2.imwrite("media/Lady_04_out.jpg", openPoseBody.outimage)
    # cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", openPoseBody.outimage)
    # cv2.waitKey(0)

if __name__ == '__main__':

    req = {
        "input":'media/Lady_04.jpg',
        "output":'media/Lady_04_out.jpg',
        "targetPoints": ["head", "hip"],
        "leftPadding": [80, 100],
        "topPadding": [80, 110],
    }
    RunProcess(None)
