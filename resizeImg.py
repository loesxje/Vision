import cv2
import numpy as np

import avansvisionlib as avl

import os

testOrTrain = "train" + "Old"

imageWD = 'C:\Visionplaatje\\numbers\\{}\\'.format(testOrTrain)

maxRow = 94
maxCol = 88

#Haal de afbeeldingen uit de map.
for file in os.listdir(imageWD): # +folder
    if file != ".DS_Store":
        filename = imageWD + file
        image = cv2.imread(filename)
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        binaryImage = cv2.threshold(grayImage, 160, 255, cv2.THRESH_BINARY)[1]
        nRows = binaryImage.shape[0]
        nCols = binaryImage.shape[1]
        
        empty = np.ones((maxRow,maxCol))*255
        
        diffRow = maxRow-nRows
        diffCol = maxCol-nCols
        if not(diffRow == 0 and diffCol == 0):
            
            if diffRow % 2 == 0:
                offSetRow = diffRow/2
                endSetRow = diffRow/2
            else:
                offSetRow = np.floor(diffRow/2)
                endSetRow = np.ceil(diffRow/2)
                
            if diffCol % 2 == 0:
                offSetCol = diffCol/2
                endSetCol = diffCol/2
            else:
                offSetCol = np.floor(diffCol/2)
                endSetCol = np.ceil(diffCol/2)
            
            rowRange = range(offSetRow, maxRow-endSetRow)
            colRange = range(offSetCol, maxCol-endSetCol)
            
            rowIterate = 0
            for rows in rowRange:
                empty[rows-1][colRange] = binaryImage[rowIterate]
                rowIterate += 1
                
            
            cv2.imwrite(filename, empty)
            print("{} done resizing".format(filename))
            