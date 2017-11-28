import numpy as np
 
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
	
	
def findNextBlob(admin):
    global row, col
    found = False
    adminshp = admin.shape

    # Search in current row and so on
    nrow = adminshp[0]
    ncol = adminshp[1]
    while not found:
        for currRow in range(row, nrow - 1):
            for currCol in range(ncol - 1):
                if (admin[currRow][currCol] == -1):
                    found = True
                    row = currRow
                    col = currCol

    if (not found):
        row = -1
        col = -1
    return found
	
def labelIter(admin, blobNr):
	x = row
	y = col
	admin[x][y] = blobNr*10 + 8
	
	next1 = -999
	area = 1
	
	allLabeledFlag = True
	while(allLabeledFlag):
		allLabeledFlag = False
		pathLabeled = False
		while not (pathLabeled):
			if(not allLabeledFlag):
				allLabeledFlag = moreNext1(admin, x, y)
				findNext1(admin, x, y, next1)
				
			if(next1 >= 0):
				admin[x][y] = blobNr*10 + next1
				area += area
				
			else:
				findPrevious = admin[x][y] % 10
				if(findPrevious = 0):
					x += 1
					break
				ifelse(findPrevious = 1):
					x += 1
					y -= 1
					break
				ifelse(findPrevious = 2):
					y -= 1
					break;
				ifelse(findPrevious = 3):
					x -= 1
					y -= 1
					break
				ifelse(findPrevious = 4):
					x -= 1
					break
				ifelse(findPrevious = 5):
					x -= 1
					y += 1
					break
				ifelse(findPrevious = 6):
					y += 1
					break
				ifelse(findPrevious = 7):
					x += 1
					y += 1
				ifelse(pathLabeled = True):
					break
				else:
					print "Error func labelIter!"
	return area
	

