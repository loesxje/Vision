import numpy as np
import cv2
from skimage import measure

def printMatrix(m):
    [row,col] = np.shape(m)
    for jj in range(row):
        print m[jj,:]

def setValue(m, value):
    shapeM = np.shape(m)
    m = np.ones(shapeM)*value
    return m

def inproduct(A, B):
    s = 0
    dimA = A.shape
    dimB = B.shape
    if dimA != dimB:
        print "Vectors or matrices must have the same length"

    if len(dimA) == 2:
        row = dimA[0]
        col = dimA[1]
        for i in range(row):
            for j in range(col):
                s += A[i][j] * B[i][j]
    else:
        lengthA = len(A)
        for i in range(lengthA):
            s += A[i] * B[i]
    return s

def addMatrices(a, b):
    result = np.zeros([a.shape[0], a.shape[1]])
    for row in range(a.shape[0]):
        for col in range(a.shape[1]):
            result[row][col] = a[row][col] + b[row][col]
    return result

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
            newValue = np.floor(scale*(oldValue - minValue)) + minPixelValue
            m[ii][jj]= newValue
            
    return m

def show16SImageStretch(m, windowName):
    mCopy = m.copy()
    mCopy = stretchImage(mCopy, 0, 255)
    cv2.imshow(windowName, mCopy)
    cv2.waitKey(0)
    

def gammaCorrection(img, correction): #only for 1 channel pictures
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

def findNextBlob(admin, row, col):
    found = False
    adminshp = admin.shape

    # Search in current row and so on
    nrow = adminshp[0]
    ncol = adminshp[1]
    
    for currCol in range(col, ncol -1):
        if (admin[row][currCol] == -1):
                found = True
                col = currCol
                break
        if found:
            break
        
    for currRow in range(row+1, nrow - 1):
        for currCol in range(1, ncol - 1):
            if (admin[currRow][currCol] == -1):
                found = True
                row = currRow
                col = currCol
                break
        if found:
            break

    if (not found):
        row = -1
        col = -1
    return [found, row, col]


def getEntryNeighbour(admin, row, col, mooreNr):

    switch = {
            0: admin[row][col-1],
            1: admin[row+1][col-1],
            2: admin[row-1][col],
            3: admin[row+1][col+1],
            4: admin[row][col+1],
            5: admin[row-1][col+1],
            6: admin[row-1][col],
            7: admin[row-1][col-1]
            }
    return switch.get(mooreNr, "ERROR getEntryNeighbour")

def moreNext1(admin, row, col):

    more = False
    count = 0
    for ii in range(7):
        if getEntryNeighbour(admin, row, col, ii)== -1:
            count += 1
            
        if count > 1:
            more = True
    return more

def checkAdmin(admin, row, col):
    if admin[row][col] == -1:
        return True
    else:
        return False

def findNext1(admin, row, col):
    
    
    rotRow = row-1
    rotCol = col
    
    if checkAdmin(admin, rotRow, rotCol):
        nextMooreNr = 0
    else:
        rotRow = row-1
        rotCol = col+1
        if checkAdmin(admin, rotRow, rotCol):
            nextMooreNr = 1
        else:
            rotRow = row
            rotCol = col+1
            if checkAdmin(admin, rotRow, rotCol):
                nextMooreNr = 2
            else:
                rotRow = row+1
                rotCol = col+1
                if checkAdmin(admin, rotRow, rotCol): 
                    nextMooreNr = 3
                else:
                    rotRow = row+1
                    rotCol = col
                    if checkAdmin(admin, rotRow, rotCol): 
                        nextMooreNr = 4
                    else:
                        rotRow = row+1
                        rotCol = col-1
                        if checkAdmin(admin, rotRow, rotCol): 
                            nextMooreNr = 5
                        else:
                            rotRow = row
                            rotCol = col-1
                            if checkAdmin(admin, rotRow, rotCol): 
                                nextMooreNr = 6
                            else:
                                rotRow = row-1
                                rotCol = col-1
                                if checkAdmin(admin, rotRow, rotCol): 
                                    nextMooreNr = 7
                                else:
                                    nextMooreNr = -99
    if nextMooreNr >= 0:
        row = rotRow
        col = rotCol
    return [row, col, nextMooreNr]


# =============================================================================
# def labelIter(admin, row, col, blobNr):
#     
# 	admin[row][col] = blobNr*10 + 8
# 	
# 	next1 = -999
# 	area = 1
# 	allLabeledFlag = True
# 	while allLabeledFlag:
# 	    allLabeledFlag = False
#         pathLabeled = False
#         while not (pathLabeled):    
#             if(not allLabeledFlag):
#                 allLabeledFlag = moreNext1(admin, row, col)
#             [row, col, next1] = findNext1(admin, row, col)
# 			
#             if(next1 >= 0):
#                 admin[row][col] = blobNr*10 + next1
#                 area += 1
# 
#             else:
#                 findPrevious = admin[row][col] % 10
#                 if findPrevious == 0:
#                     row += 1
#                     break
#                 elif(findPrevious == 1):
#     					row += 1
#     					col -= 1
#     					break
#                 elif(findPrevious == 2):
#     					col -= 1
#     					break;
#                 elif(findPrevious == 3):
#     					row -= 1
#       					col -= 1
#       					break
#                 elif(findPrevious == 4):
#                     row -= 1
#                     break
#                 elif(findPrevious == 5):
#                     row -= 1
#                     col += 1
#                     break
#                 elif(findPrevious == 6):
#                     col += 1
#                     break
#                 elif(findPrevious == 7):
#                     row += 1
#                     col += 1
#                 elif findPrevious == 8:
#                     (pathLabeled) = True
#                     break
#                 else:
#                     print "Error func labelIter!"
# 	return [admin, area]
# 
# def labelIterInfo(admin, topRow, topCol, blobNr):
#     rowGravity = topRow
#     colGravity = topCol
#     row = topRow
#     col = topCol
#     admin[row][col] = blobNr * 10 + 8
#     area = 1
#     
#     allLabeledFlag = True
#     while (allLabeledFlag):
#         allLabeledFlag = False
#         pathLabeled = False
#         while not (pathLabeled):    
#             if(not allLabeledFlag):
#                 allLabeledFlag = moreNext1(admin, row, col)
#                 [row, col, next1] = findNext1(admin, row, col)
# 			
#             if(next1 >= 0):
#                 admin[row][col] = blobNr*10 + next1
#                 area += 1
# 
#             else:
#                 findPrevious = admin[row][col] % 10
#                 if findPrevious == 0:
#                     row += 1
#                     break
#                 elif(findPrevious == 1):
#     					row += 1
#     					col -= 1
#     					break
#                 elif(findPrevious == 2):
#     					col -= 1
#     					break;
#                 elif(findPrevious == 3):
#     					row -= 1
#       					col -= 1
#       					break
#                 elif(findPrevious == 4):
#                     row -= 1
#                     break
#                 elif(findPrevious == 5):
#                     row -= 1
#                     col += 1
#                     break
#                 elif(findPrevious == 6):
#                     col += 1
#                     break
#                 elif(findPrevious == 7):
#                     row += 1
#                     col += 1
#                 elif findPrevious == 8:
#                     (pathLabeled) = True
#                     break
#                 else:
#                     print "Error func labelIter!"
#     rowGravity = rowGravity /area
#     colGravity = colGravity /area
#     return [admin, area, rowGravity, colGravity]
# =============================================================================


def labelRecursive(admin, row, col, blobNr):
    area = 0
    if admin[row][col] == -1:
        admin[row][col] = blobNr
        area = 1
        
        # alle pixels rondom huidige pixel bezoeken
		# (row-1,col-1) (row-1,col ) (row-1,col+1) 
		# (row  ,col-1) (row,  col ) (row  ,col+1)
		# (row+1,col-1) (row,  col ) (row+1,col+1)
        area += labelRecursive(admin, row - 1, col, blobNr)
        area += labelRecursive(admin, row - 1, col + 1, blobNr)
        area += labelRecursive(admin, row, col + 1, blobNr)
        area += labelRecursive(admin, row + 1, col + 1, blobNr)
        area += labelRecursive(admin, row, col, blobNr)
        area += labelRecursive(admin, row + 1, col - 1, blobNr)
        area += labelRecursive(admin, row, col - 1, blobNr)
        area += labelRecursive(admin, row - 1, col - 1, blobNr)
    return [admin, area]

def retrieveLabeledImage(admin):
    [adminRow, adminCol] = np.shape(admin)
    labeledImage = np.zeros([adminRow-2, adminCol-2])
    
    for ii in range(1,adminRow-1):
        for jj in range(1,adminCol-1):
            labeledImage[ii-1][jj-1] = admin[ii][jj]/10
    return labeledImage

# =============================================================================
# def labelBLOBs(binaryImage):
#     admin = makeAdmin(binaryImage)
# 
#     [adminRow, adminCol] = np.shape(admin)
#     labeledImage = np.zeros([adminRow-2, adminCol-2])
# 
#     row = 1
#     col = 1
#     blobNr = 0
#     
#     while ((row > 0) & (row < (adminRow - 1)) & (col > 0) & (col < (adminCol - 1))):
#         [found, row, col] = findNextBlob(admin, row, col)
#         if found:
#             blobNr += 1
#             [admin, area] = labelIter(admin, row, col, blobNr)
#     labeledImage = retrieveLabeledImage(admin)
#     
#     return [blobNr, labeledImage]
# 
# =============================================================================
def removeBLOB(admin, blobNr):
    [adminRow, adminCol] = np.shape(admin)
    for ii in range(1, adminRow):
        for jj in range(1, adminCol):
            value = admin[ii][jj]
            while value > 10:
                value = value/10
            if value == blobNr:
                admin[ii][jj] = 0
                
    return admin


# =============================================================================
# def labelBLOBsInfo(binaryImage, labeledImage, thresAreaMin, threshAreaMax):
#     admin = makeAdmin(binaryImage)
#     row = 1
#     col = 1
#     blobNr = 0
#     firstpixelVec = []
#     posVec = []
#     areaVec = []
#     while ((row > 0 & row < (admin.reshape[0] - 1))
#                & (col > 0) & (col < (admin.reshape[1] - 1))):
#         if findNextBlob(admin):
#             blobNr += 1
#             [admin, area, xGravity, yGravity] = labelIterInfo(admin, row, col, blobNr)
#             if (area >= thresAreaMin & area <= threshAreaMax):
#                 firstpixelVec.append([row - 1, col - 1])
#                 posVec.append([xGravity - 1, yGravity - 1])
#                 areaVec.append(area)
#             else:
#                 blobNr -= 1
#                 removeBLOB(admin, blobNr)
# 
#     retrieveLabeledImage(admin, labeledImage)
# 
#     return blobNr
# =============================================================================

def makeContourImage(binaryImage, inner = True):
    if inner:
        binaryImage = cv2.erode(binaryImage.copy(), kernel = np.ones([3,3]))
    contours = measure.find_contours(binaryImage, level = 0., fully_connected = "high", positive_orientation = "high")
    contourImage = np.zeros(np.shape(binaryImage))
    contourVec = {}
    for ii in range(len(contours)):
        numCor = len(contours[ii])
        corIndex = range(numCor)
        tempArray = np.zeros([numCor,2])
        
        for jj in corIndex:
            cor = contours[ii][jj]
            row = int(cor[0])
            col = int(cor[1])
            contourImage[row][col] = 1
#            if not ([row, col] in tempArray):
            tempArray[jj] = [row, col]
        contourVec[ii] = tempArray
    
                
    return [contourImage, contourVec]

def contourFourConnected(contourImage, labeledImage):
    # possible missing corners
#    missingCorners = np.array([np.matrix('0 0; 0 1'), np.matrix('0 0; 1 0'), np.matrix('0 1; 0 0'), np.matrix('1 0; 0 0')]) 
#    missingCornersBot = np.array([np.matrix('0 1; 0 0'), np.matrix('1 0; 0 0')])
    #add outer row of zeros and cols 
    copyContourImage = contourImage.copy()
    [row,col] = np.shape(contourImage)
    contourLabeled = np.zeros([row+2, col+2], dtype = int)
    innerContour = contourImage + labeledImage
    contourLabeled[1:row+1, 1:col+1] = innerContour
    
    #scan every cell for a possible corner
    for rowIndex in range(1, row+1):
        for colIndex in range(1, col+1):                
            scanMatrix = np.int32(np.zeros([2,2]))
            scanMatrix[0,0] = contourLabeled[rowIndex, colIndex]
            scanMatrix[0,1] = contourLabeled[rowIndex, colIndex+1]
            scanMatrix[1,0] = contourLabeled[rowIndex+1, colIndex]
            scanMatrix[1,1] = contourLabeled[rowIndex+1, colIndex+1]
            if np.any(scanMatrix):
                if scanMatrix[1,1] == 1 and scanMatrix[0,0] == 0 and scanMatrix[1,0] == 0 and scanMatrix[0,1] == 0:
                    copyContourImage[rowIndex, colIndex] = 1
#                    print "contour filled at row {} and col {}".format(rowIndex, colIndex)
                elif scanMatrix[1,0] == 1 and scanMatrix[0,0] == 0 and scanMatrix[1,1] == 0 and scanMatrix[0,1] == 0:
                    copyContourImage[rowIndex, colIndex-1] = 1
#                    print "contour filled at row {} and col {}".format(rowIndex, colIndex)
                elif scanMatrix[0,1] == 1 and scanMatrix[0,0] == 0 and scanMatrix[1,0] == 0 and scanMatrix[1,1] == 0:
                    copyContourImage[rowIndex-1, colIndex] = 1
#                    print "contour filled at row {} and col {}".format(rowIndex, colIndex)
                elif scanMatrix[0,0] == 1 and scanMatrix[1,1] == 0 and scanMatrix[1,0] == 0 and scanMatrix[0,1] == 0:
                    copyContourImage[rowIndex-1, colIndex-1] = 1
#                    print "contour filled at row {} and col {}".format(rowIndex, colIndex)
    return copyContourImage
