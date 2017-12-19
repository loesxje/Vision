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
    if "zero" in filename:
        OT = [0,0,0,0]
    elif "one" in filename:
        OT = [0,0,0,1]
    elif "two" in filename:
        OT = [0,0,1,0]
    elif "three" in filename:
        OT = [0,0,1,1]
    elif "four" in filename:
        OT = [0,1,0,0]
    elif "five" in filename:
        OT = [0,1,0,1]
    elif "six" in filename:
        OT = [0,1,1,0]
    elif "seven" in filename:
        OT = [0,1,1,1]
    elif "eight" in filename:
        OT = [1,0,0,0]
    elif "nine" in filename:
        OT = [1,0,0,1]
    else:
        raise valueError("Could not correctly classify object.")

    return OT