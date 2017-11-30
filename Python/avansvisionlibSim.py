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

def findNextBlob(admin, row, col):
    found = False
    adminshp = admin.shape

    # Search in current row and so on
    nrow = adminshp[0]
    ncol = adminshp[1]
    while not found:
        for currRow in range(row, nrow - 1):
            for currCol in range(col, ncol - 1):
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


def getEntryNeighbour(admin, x, y, mooreNr):

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

    more = False
    
    for ii in range(7):
        if getEntryNeighbour(admin, x, y, ii)== -1:
            more = True
            break
    return more

def checkAdmin(admin, funX, funY):
    if admin[funY][funX] == -1:
        return True
    else:
        return False

def findNext1(admin, x, y):
    
    rotX = x-1
    rotY = y
    
    if checkAdmin(admin, rotX, rotY):
        nextMooreNr = 0
    else:
        rotX = x-1
        rotY = y-1
        if checkAdmin(admin, rotX, rotY):
            nextMooreNr = 1
        else:
            rotX = x
            rotY = y-1
            if checkAdmin(admin, rotX, rotY):
                nextMooreNr = 2
            else:
                rotX = x+1
                rotY = y-1
                if checkAdmin(admin, rotX, rotY): 
                    nextMooreNr = 3
                else:
                    rotX = x+1
                    rotY = y
                    if checkAdmin(admin, rotX, rotY): 
                        nextMooreNr = 4
                    else:
                        rotX = x+1
                        rotY = y+1
                        if checkAdmin(admin, rotX, rotY): 
                            nextMooreNr = 5
                        else:
                            rotX = x
                            rotY = y+1
                            if checkAdmin(admin, rotX, rotY): 
                                nextMooreNr = 6
                            else:
                                rotX = x-1
                                rotY = y+1
                                if checkAdmin(admin, rotX, rotY): 
                                    nextMooreNr = 7
                                else:
                                    print "no neighbour found"
    if nextMooreNr >= 0:
        x = rotX
        y = rotY
    return [x, y, nextMooreNr]


def labelIter(admin, row, col, blobNr):
	x = row
	y = col
	admin[y][x] = blobNr*10 + 8
	
	next1 = -999
	area = 1
	
	allLabeledFlag = True
	while(allLabeledFlag):
		allLabeledFlag = False
		pathLabeled = False
		while not (pathLabeled):
			if(not allLabeledFlag):
				allLabeledFlag = moreNext1(admin, x, y)
				[x, y, next1] = findNext1(admin, x, y)
				
			if(next1 >= 0):
				admin[y][x] = blobNr*10 + next1
				area += 1
				
			else:
				findPrevious = admin[y][x] % 10
				if findPrevious == 0:
					x += 1
					break
				elif(findPrevious == 1):
					x += 1
					y -= 1
					break
				elif(findPrevious == 2):
					y -= 1
					break;
				elif(findPrevious == 3):
					x -= 1
					y -= 1
					break
				elif(findPrevious == 4):
					x -= 1
					break
				elif(findPrevious == 5):
					x -= 1
					y += 1
					break
				elif(findPrevious == 6):
					y += 1
					break
				elif(findPrevious == 7):
					x += 1
					y += 1
				elif(pathLabeled):
					break
				else:
					print "Error func labelIter!"
	return [admin, area]

def labelIterInfo(admin, topX, topY, blobNr):
    xGravity = topX
    yGravity = topY
    x = topX
    y = topY
    admin[y][x] = blobNr * 10 + 8
    area = 1
    
    allLabeledFlag = True
    while (allLabeledFlag):
        allLabeledFlag = False
        pathLabeled = False
        while not (pathLabeled):    
            if(not allLabeledFlag):
                allLabeledFlag = moreNext1(admin, x, y)
                [x, y, next1] = findNext1(admin, x, y)
			
            if(next1 >= 0):
                admin[x][y] = blobNr*10 + next1
                area += 1

            else:
                findPrevious = admin[x][y] % 10
                if findPrevious == 0:
                    x += 1
                    break
                elif(findPrevious == 1):
    					x += 1
    					y -= 1
    					break
                elif(findPrevious == 2):
    					y -= 1
    					break;
                elif(findPrevious == 3):
    					x -= 1
      					y -= 1
      					break
                elif(findPrevious == 4):
                    x -= 1
                    break
                elif(findPrevious == 5):
                    x -= 1
                    y += 1
                    break
                elif(findPrevious == 6):
                    y += 1
                    break
                elif(findPrevious == 7):
                    x += 1
                    y += 1
                elif(pathLabeled):
                    break
                else:
                    print "Error func labelIter!"
    xGravity = xGravity /area
    yGravity = yGravity /area
    return [admin, area, xGravity, yGravity]

# =============================================================================
#    This was a gitmistake. Accidentally copied both versions.
#    Need to check if there are differences and which one is right.
# def labelIter(admin, blobNr, row, col):
#     x = row
#     y = col
#     admin[x][y] = blobNr * 10 + 8
# 
#     next1 = -999
#     area = 1
# 
#     allLabeledFlag = True
#     while (allLabeledFlag):
#         allLabeledFlag = False
#         pathLabeled = False
#         while not (pathLabeled):
#             if (not allLabeledFlag):
#                 allLabeledFlag = moreNext1(admin, x, y)
#                 [x, y, next1] = findNext1(admin, x, y)
# 
#             if (next1 >= 0):
#                 admin[x][y] = blobNr * 10 + next1
#                 area += area
# 
#             else:
#                 findPrevious = admin[x][y] % 10
#                 if (findPrevious == 0):
#                     x += 1
#                     break
#                 elif(findPrevious == 1):
#                     x += 1
#                     y -= 1
#                     break
#                 elif(findPrevious == 2):
#                     y -= 1
#                     break
#                 elif(findPrevious == 3):
#                     x -= 1
#                     y -= 1
#                     break
#                 elif(findPrevious == 4):
#                     x -= 1
#                     break
#                 elif(findPrevious == 5):
#                     x -= 1
#                     y += 1
#                     break
#                 elif(findPrevious == 6):
#                     y += 1
#                     break
#                 elif(findPrevious == 7):
#                     x += 1
#                     y += 1
#                 elif(pathLabeled):
#                     break
#                 else:
#                     print "Error func labelIter!"
#     return [admin, area]
# 
# def labelIterInfo(admin, topX, topY, blobNr):
#     
#     xGravity = topX
#     yGravity = topY
#     x = topX
#     y = topY
#     admin[y][x] = blobNr*10 + 8
#     area = 1
# 
#     allLabeledFlag = True
#     while (allLabeledFlag):
#         allLabeledFlag = False
#         pathLabeled = False
#         while not (pathLabeled):
#             if (not allLabeledFlag):
#                 allLabeledFlag = moreNext1(admin, x, y)
#                 [x, y, next1] = findNext1(admin, x, y)
# 
#             if (next1 >= 0):
#                 admin[x][y] = blobNr * 10 + next1
#                 area += area
#                 xGravity += x
#                 yGravity += y
# 
#             else:
#                 findPrevious = admin[x][y] % 10
#                 if (findPrevious == 0):
#                     x += 1
#                     break
#                 elif (findPrevious == 1):
#                     x += 1
#                     y -= 1
#                     break
#                 elif (findPrevious == 2):
#                     y -= 1
#                     break
#                 elif (findPrevious == 3):
#                     x -= 1
#                     y -= 1
#                     break
#                 elif (findPrevious == 4):
#                     x -= 1
#                     break
#                 elif (findPrevious == 5):
#                     x -= 1
#                     y += 1
#                     break
#                 elif (findPrevious == 6):
#                     y += 1
#                     break
#                 elif (findPrevious == 7):
#                     x += 1
#                     y += 1
#                 elif (pathLabeled):
#                     break
#                 else:
#                     print "Error func labelIterInfo!"
#     xGravity /= area
#     yGravity /= area
#     return [admin, area, xGravity, yGravity]
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

def labelBLOBs(binaryImage):
    admin = makeAdmin(binaryImage)

    [adminRow, adminCol] = np.shape(admin)
    labeledImage = np.zeros([adminRow-2, adminCol-2])

    row = 1
    col = 1
    blobNr = 0
    
    while ((row > 0) & (row < (adminRow - 1)) & (col > 0) & (col < (adminCol - 1))):
        [found, row, col] = findNextBlob(admin, row, col)
        if found:
            blobNr += 1
            [admin, area] = labelIter(admin, row, col, blobNr)
    labeledImage = retrieveLabeledImage(admin)
    
    return [blobNr, labeledImage]

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


def labelBLOBsInfo(binaryImage, labeledImage, thresAreaMin, threshAreaMax):
    admin = makeAdmin(binaryImage)
    row = 1
    col = 1
    blobNr = 0
    firstpixelVec = {}
    posVec = {}

    while ((row > 0 & row < (admin.reshape[0] - 1))
               & (col > 0) & (col < (admin.reshape[1] - 1))):
        if findNextBlob(admin):
            blobNr += 1
            area = labelIterInfo(admin, xGravity, yGravity, blobNr)
            if (area >= thresAreaMin & area <= threshAreaMax):
                firstpixelVec.append([row - 1, col - 1])
                posVec.append([xGravity - 1, yGravity - 1])
                areaVec.append(area)
            else:
                blobNr -= 1
                removeBLOB(admin, blobNr)

    retrieveLabeledImage(admin, labeledImage)

    return blobNr
