import numpy as np

def determinePath(mooreIteration, moorePoint, currentCell):
    mooreNr = mooreIteration % 8
    
    if mooreNr == 0:
        step = np.array([-1, 0])
        moorePoint = currentCell + np.array([-1, 1])
        
    elif mooreNr == 1:
        step = np.array([-1,-1])
        moorePoint = currentCell + np.array([-1, 0])
        
    elif mooreNr == 2:
        step = np.array([0,-1])
        moorePoint = currentCell + np.array([-1,-1])

    elif mooreNr == 3:
        step = np.array([1,-1])
        moorePoint = currentCell + np.array([0,-1])
        
    elif mooreNr == 4:
        step = np.array([1, 0])
        moorePoint = currentCell + np.array([ 1,-1])
        
    elif mooreNr == 5:
        step = np.array([1, 1])
        moorePoint = currentCell + np.array([1,0])
        
    elif mooreNr == 6:
        step = np.array([0, 1 ])
        moorePoint = currentCell + np.array([1,1 ])
        
    elif mooreNr == 7:
        step = np.array([-1, 1])
        moorePoint = currentCell + np.array([ 0,1 ])
    return [step, moorePoint]

def determineMooreNr(moorePoint, currentCell):
    stepDifference = list(moorePoint - currentCell)
    mooreNr = -1
    
    if (stepDifference == [ -1, 0]):
        # the location of c0 in perspective of the currentCell b0
        mooreNr = 0;

    elif (stepDifference == [ -1, -1]):
        mooreNr = 1;

    elif (stepDifference == [ 0, -1]):
        mooreNr = 2;

    elif (stepDifference == [ 1, -1]):
        mooreNr = 3;

    elif (stepDifference == [ 1, 0]):
        mooreNr = 4;

    elif (stepDifference == [ 1, 1]):
        mooreNr = 5;

    elif (stepDifference == [ 0, 1]):
        mooreNr = 6;

    elif (stepDifference == [ -1, 1]):
        mooreNr = 7;
	
    return mooreNr;

def clockwise(currentCell, labeledImage, moorePoint):
    mooreNr = determineMooreNr(moorePoint, currentCell)
    for mooreIterate in range(8):
        [step, moorePoint] = determinePath(mooreNr + mooreIterate, moorePoint, currentCell)
        
        coordinateB = currentCell + step
        if labeledImage[coordinateB[0]][coordinateB[1]] != 0:
            return [coordinateB, moorePoint]
            
        
    return -1
    

def findFirstVecs(labeledImage, totalBlobs, row, col):
    found = False
    imgShape = labeledImage.shape
    
    totalRows = imgShape[0]
    totalCols = imgShape[1]
    
    blobNr = 1
    firstVecs = []
    for currRow in range(row, totalRows):
        for currCol in range(col, totalCols):
            if np.sum(labeledImage[currRow]) == 0:
                break
            
            if labeledImage[currRow][currCol] == blobNr:
                found = True
                firstVecs.append([currRow, currCol])
                
                if blobNr == totalBlobs:
                    return firstVecs
                
                blobNr += 1
    if found:
        firstVecs = None
        return firstVecs
    
def allContours(labeledImage, totalBlobs):
    row = 0
    col = 0
    firstVecs = findFirstVecs(labeledImage, totalBlobs, row, col)
    contourVec = {}
    for N in range(totalBlobs):
        
        # find first cell where the moore algorithm needs to start
        currentCell = np.array([None, None])
        firstCell = np.array(firstVecs[N])
        
        if N == 0:
            rowContours = np.array([firstCell])
        else:
            rowContours = np.concatenate((rowContours, [firstCell]), axis = 0)
        
        ii = 0
        moorePoint = firstCell + np.array([-1, 0])
        
        while list(currentCell) != list(firstCell):
            if ii == 0:
                currentCell = firstCell
            [currentCell, moorePoint] = clockwise(currentCell, labeledImage, moorePoint)
            rowContours = np.concatenate((rowContours, [currentCell]), axis = 0)
            ii += 1
            if ii > 1000:
                break
        
        contourVec[N] = rowContours
    aantal = len(contourVec)
    
    contourImage = np.zeros(np.shape(labeledImage))
    for ii in range(len(contourVec)):
        numCor = len(contourVec[ii])
        corIndex = range(numCor)

        for jj in corIndex:
            cor = contourVec[ii][jj]
            row = int(cor[0])
            col = int(cor[1])
            contourImage[row][col] = 1
    
    return [aantal, contourImage, contourVec]