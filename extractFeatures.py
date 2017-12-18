import numpy as np
import avansvisionlib as avl
import cv2
# from IPython import get_ipython
# ipython = get_ipython()
from skimage import measure


def extractFeaturePerimeter(binaryImage):
    # function returns an integer with the perimeter (length of the contour)
    contourVec = avl.makeContourImage(binaryImage)[1]
    perimeter = 0
    for i in range(len(contourVec)):
        perimeter += len(contourVec[i])

    return perimeter

def extractFeatureArea(binaryImage):
    # function returns an integer with the area size of the region of the object
    labeledImage = measure.label(binaryImage, background=0)

    area = 0
    for col in range(len(labeledImage[0])):
        for row in range(len(labeledImage)):
            if labeledImage[row, col] == 1:
                area += 1

    return area

def extractFeatureNumberOfHoles(binaryImage):
    # function returns an integer with the number of holes in the object
    # contours

    contourVec = avl.makeContourImage(binaryImage)[1]
    NumberOfContours = len(contourVec)

    # blobs
    labeledImage = measure.label(binaryImage, background=0)
    NumberOfBlobs = np.max(labeledImage)

    NumberOfHoles = NumberOfContours - NumberOfBlobs

    return NumberOfHoles


def extractFeatureCircularity(perimeter, area):
    # (4pi*Area)/(Perimeter)
    circularity = (4*np.pi*area) / (perimeter**2)

    return circularity

def extractFeatures(binaryImage):
    perimeter = extractFeaturePerimeter(binaryImage)
    area = extractFeatureArea(binaryImage)
    nrHoles = extractFeatureNumberOfHoles(binaryImage)
    circularity = extractFeatureCircularity(perimeter, area)
    IT = [1, perimeter, area, nrHoles, circularity]
    return IT

def outputHandwrittenNumbers(filename):
    #filename = str(filename)
    if "nul" in filename:
        OT = [0,0,0,0]
    elif "een" in filename:
        OT = [0,0,0,1]
    elif "twee" in filename:
        OT = [0,0,1,0]
    elif "drie" in filename:
        OT = [0,0,1,1]
    elif "vier" in filename:
        OT = [0,1,0,0]
    elif "vijf" in filename:
        OT = [0,1,0,1]
    elif "zes" in filename:
        OT = [0,1,1,0]
    elif "zeven" in filename:
        OT = [0,1,1,1]
    elif "acht" in filename:
        OT = [1,0,0,0]
    else:
        OT = [1,0,0,1]

    return OT