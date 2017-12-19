import numpy as np
import avansvisionlib as avl
import cv2
# from IPython import get_ipython
# ipython = get_ipython()
from skimage import measure
import os
import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import exposure


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

    if NumberOfHoles == 0:
        return 0
    else:
        return (1 / NumberOfHoles)


def extractFeatureCircularity(perimeter, area):
    # (4pi*Area)/(Perimeter)
    circularity = (perimeter**2)/(4*np.pi*(area))

    return circularity

def retrieveHOG(inputMatrix, doPlot=False):
    image = inputMatrix.copy()
    fd, hogImage = hog(image, orientations=8, pixels_per_cell=(16, 16),
                       cells_per_block=(1, 1), visualise=True)

    hogVector = [0]*hogImage.size
    nRows = hogImage.shape[0]
    nCols = hogImage.shape[1]

    index = 0
    for cols in range(nCols):
        for rows in range(nRows):
            hogVector[index] = hogImage[rows][cols]
            index += 1

    return hogVector


def extractFeatures(binaryImage):
    #perimeter = extractFeaturePerimeter(binaryImage)
    #area = extractFeatureArea(binaryImage)
    #nrHoles = extractFeatureNumberOfHoles(binaryImage)
    hogVector = retrieveHOG(binaryImage, doPlot=False)
    IT = [1]
    IT.extend(hogVector)
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
        OT = [1, 0, 0, 1]
    else:
        print("Could not correctly classify object.")
    return OT

def outputToNumber(OO):
    if OO == [0,0,0,0]: numberRecognized = 0
    elif OO == [0,0,0,1]: numberRecognized = 1
    elif OO == [0,0,1,0]: numberRecognized = 2
    elif OO == [0,0,1,1]: numberRecognized = 3
    elif OO == [0,1,0,0]: numberRecognized = 4
    elif OO == [0,1,0,1]: numberRecognized = 5
    elif OO == [0,1,1,0]: numberRecognized = 6
    elif OO == [0,1,1,1]: numberRecognized = 7
    elif OO == [1,0,0,0]: numberRecognized = 8
    elif OO == [1,0,0,1]: numberRecognized = 9
    else:
        print("Could not correctly classify object.")

    return numberRecognized

def makeBinaryImage(path):
    image = cv2.imread(path)
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binaryImage = cv2.threshold(grayImage, 140, 1, cv2.THRESH_BINARY_INV)[1]
    return binaryImage

def memoriseLargest(imageWD):
    perimeterMax = 0
    areaMax = 0
    for file in os.listdir(imageWD):
        if file != ".DS_Store":
            binaryImage = makeBinaryImage(imageWD + file)
            featureArray = np.array(extractFeatures(binaryImage,1,1))
            perimeterCurrent = featureArray[1]
            areaCurrent = featureArray[2]
            if perimeterCurrent > perimeterMax:
                perimeterMax = perimeterCurrent
            if areaCurrent > areaMax:
                areaMax = areaCurrent
    return perimeterMax, areaMax