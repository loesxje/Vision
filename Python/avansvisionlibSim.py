import numpy as np
import cv2

def printMatrix(m):
    [row,col] = np.shape(m)
    for jj in range(row):
        print m[jj,:]

def setValue(m, value):
    [row,col] = np.shape(m)
    m = np.ones(row,col)*value
    return m

def setRandomValue(m, min, max):
    [row,col] = np.shape(m)
    m = np.ones(row,col)*np.random.randint(min,max,1)
    return m
    
# =============================================================================
# NB images are supposed to have 1 channel (B/W image) and depth 16 bits signed (CV_16S) 
# =============================================================================

def getPixelRangeImage(m):
    minValue = np.min(m)
    maxValue = np.max(m)
    return [minValue, maxValue]    

def stretchImage(m, minPixelValue, maxPixelValue):
    [minValue, maxValue] = getPixelRangeImage(m)
    scale = (maxPixelValue - minPixelValue)/(maxValue - minValue)
    [row,col] = np.shape(m)
    for ii in range(row):
        for jj in range(col):
            oldValue = m[ii][jj]
            newValue = scale*(oldValue - minValue) + minPixelValue
            m[ii][jj]= newValue
            
    return m

def show16SImageStretch(m, windowName):
    mCopy = m
    mCopy = stretchImage(mCopy, 0, 255)
    cv2.imshow(windowName, mCopy)
    cv2.waitKey(0)  

def gammaCorrection(img, correction):
    img = img/255.0
    img = cv2.pow(img, correction)
    return img*255

def makeAdmin(binImg):
    [row,col] = np.shape(binImg)
    
    result = np.zeros([row+2, col+2], dtype = int)
    
    zerosArray = np.zeros(col+2)
    result[0][:] = zerosArray
    
    for ii in range(1,row):
        result[ii][0] = 0
        for jj in range(col):
            if binImg[ii-1][jj-1]>=1:
                result[ii][jj] = -1
        result[ii][col+1] = 0
    result[result.shape[0]-1][:] = zerosArray
    return result

def getEntryNeighbour(admin, x, y, mooreNr):
    x -= 1
    y -= 1
    switch = {
            0: admin[y][x-1],
            1: admin[y-1][x-1],
            2: admin[y-1][x],
            3: admin[y-1][x+1],
            4: admin[y][x+1],
            5: admin[y+1][x+1],
            6: admin[y+1][x],
            7: admin[y+1][x-1]
            }
    return switch.get(mooreNr, "ERROR getEntryNeighbour")

def moreNext1(admin, x, y):
    x -= 1
    y -= 1
    more = False
    
    for ii in range(7):
        if getEntryNeighbour(admin, x, y, ii)== -1:
            more = True
            break
    return more

def findNext1(admin, x, y, nextMooreNr):
    global
    
    
    
    switch = {
            0: admin[y][x-1],
            1: admin[y-1][x-1],
            2: admin[y-1][x],
            3: admin[y-1][x+1],
            4: admin[y][x+1],
            5: admin[y+1][x+1],
            6: admin[y+1][x],
            7: admin[y+1][x-1]
            }
