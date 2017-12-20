import cv2
import numpy as np
import avlBPNEvaWorking as BPN
import avansvisionlib as avl
import pandas as pd
import os
import extractFeatures as ef

def testHandwrittenNumbers(imageWD, V0, W0):
    imageCodes = []

    for file in os.listdir(imageWD):  # +folder
        if file != ".DS_Store":
            numberOfInputs = len(os.listdir(imageWD))
            imageCodes.append(file)

    print(imageCodes)
    perimeterMax, areaMax = ef.memoriseLargest(imageWD)

    for i in range(len(imageCodes)):
        
        filename = imageCodes.pop(0)
        print(filename)
        image = cv2.imread(imageWD + filename)
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        binaryImage = cv2.threshold(grayImage, 140, 1, cv2.THRESH_BINARY_INV)[1]
        IT = np.array(ef.extractFeatures(binaryImage))
        
        OO = np.array(BPN.BPN(IT,V0,W0))
        #OO = np.round(np.round(OO,1))
        print(OO)

# def confusionMatrix(imageWDTest, OO):
#     realOutput = ["five"] #alle 20 de images
#     confusionMat = np.zeros((10,10))
#     for file in os.listdir(imageWDTest):
#         if file != ".DS_Store":
#             for i in range(len(os.listdir(imageWDTest))): #pakt op volgorde
#                 filename = "numbersTest_%d.jpg", i
#                 confusionMat[realOutput[i],OO[i]] += 1
