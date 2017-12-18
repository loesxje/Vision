import numpy as np
import cv2
import avansvisionlib as avl
from IPython import get_ipython
ipython = get_ipython()
from skimage import measure


def extractFeaturePerimeter(binaryImage):
    # function returns an integer with the perimeter (length of the contour)
    contourVec = avl.makeContourImage(binaryImage)[1]
    perimeter = len(contourVec[0]) + len(contourVec[1])

    return perimeter

def extractFeatureArea(binaryImage):
    # function returns an integer with the area size of the region of the object
    labeledImage = measure.label(binaryImage, background=0)

    areaVector = []
    for col in range(len(labeledImage[0])):
        for row in range(len(labeledImage)):
            if labeledImage[row, col] == 1:
                areaVector.append(1)
    area = len(areaVector)

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






