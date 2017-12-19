import numpy as np
import cv2


#Make bounding boxes

#func:  delivers bounding boxes of def contours
#pre:   def contours contains the contours for which bounding boxes have to be delivered
#post:  bbs contains all bounding boxes. The index corresponds to the index of contours.
#           i.e. bbs[i] belongs to contours[i]

def allBoundingBoxes(contourvector):
    #argument contourvector comes from makeContourImage

    #for i in size(findNextBlob):
        #calc min_x & min_y from the contour of every Blob
        #calc max_x & max_y from the contour of every Blob
    bbs = []
    
    
    for i in range(len(contourvector)):
        allRow = []
        allCol = []
        blobContour = contourvector[i]
        for rowColIndex in range(len(blobContour)):
            allRow.append(blobContour[rowColIndex][0])
            allCol.append(blobContour[rowColIndex][1])
        
        minRow = min(allRow)
        maxRow = max(allRow)
        
        minCol = min(allCol)
        maxCol = max(allCol)
        minCor = (minRow, minCol)
        maxCor = (maxRow, maxCol)
# =============================================================================
#         minCor = (bbox._min[0], bbox._min[1]) #tuple(minRow, minCol)
#         maxCor = (bbox._max[0], bbox._max[1]) #tuple(maxRow, maxCol)
# =============================================================================
        bbs.append([minCor, maxCor])
    return bbs

def biggestBoundingBox(boundingBoxesVector):
    #calc difference min_x & max_x & min_y & max_y
    rowDifference = 0
    colDifference = 0
    for i in range(len(boundingBoxesVector)):
        rowDif = boundingBoxesVector[i][1][0] - boundingBoxesVector[i][0][0]
        colDif = boundingBoxesVector[i][1][1] - boundingBoxesVector[i][0][1]
        if(rowDif > rowDifference):
            rowDifference = rowDif
        if(colDif > colDifference):
            colDifference = colDif

    #make the length of the biggest bounding box odd. This way, it is easier to define a middle
    if(rowDifference%2 == 0):
        rowDifference += 1
    if(colDifference%2 == 0):
        colDifference += 1

    #save greatest difference x & y
    biggestBoBo = [rowDifference, colDifference]

    return biggestBoBo

def getCoordinatesAllBoundingBoxes(allBoBo, biggestBoBo, image, doPlot = 1):
    #start in the middle of the Blob
    middle = []
    
    rangeRows = [0] # initial number for iteration. This will be deleted in the
    rangeCols = [0] # first try
    
    for i in range(len(allBoBo)):
        notFound = False
        maxRow = allBoBo[i][1][0]
        minRow = allBoBo[i][0][0]

        maxCol = allBoBo[i][1][1]
        minCol = allBoBo[i][0][1]
        
        width = int(np.ceil((maxRow-minRow)))
        height = int(np.ceil((maxCol-minCol)))
        
        midRow = (((maxRow - minRow) / 2) + minRow)
        midCol = (((maxCol - minCol) / 2) + minCol)
        tempRangeRow = range(int(np.floor(midRow))-width, int(np.ceil(midRow))+height)
        tempRangeCol = range(int(np.floor(midCol))-width, int(np.ceil(midCol))+height)

        for elem in range(len(rangeRows)):
            if i == 0:
                rangeRows.pop() #remove initial number
                rangeCols.pop()
                rangeRows.append(tempRangeRow)
                rangeCols.append(tempRangeCol)
                middle.append([midRow, midCol])
                break
            elif int(np.floor(midRow)) in rangeRows[elem] and int(np.floor(midCol)) in rangeCols[elem]:
                notFound = False
                break
            else:
                notFound = True
                
        if notFound:
            rangeRows.append(tempRangeRow)
            rangeCols.append(tempRangeCol)
            middle.append([midRow, midCol])
            
            
    #find boxpoints per blob that exist within the imagesize
    boxPoints = []
    for i in range(len(middle)):
        startRow= int(np.ceil(middle[i][0] - 0.5 * biggestBoBo[0]))
        endRow = int(np.ceil(middle[i][0] + 0.5 * biggestBoBo[0]))

        if(startRow < 0):
            endRow += startRow * -1 # negative * -1 = positive
            startRow = 0
        elif(endRow > image.shape[0]):
            startRow += int(np.ceil(image.shape[0])) - endRow
            endRow = int(np.ceil(image.shape[0]))

        startCol = int(np.ceil(middle[i][1] - 0.5 * biggestBoBo[1]))
        endCol = int(np.ceil(middle[i][1] + 0.5 * biggestBoBo[1]))

        if(startCol < 0):
            endCol += startCol * -1
            startCol = 0
        elif(endCol > image.shape[1]):
            startCol += (int(np.ceil(image.shape[1])) -endCol)
            endCol = int(np.ceil(image.shape[1]))

        boxPoints.append([[startRow, startCol], [endRow, endCol]])
        
    if doPlot:
        for blobNr in range(1, len(boxPoints)+1):
            [[startRow, startCol], [endRow, endCol]] = boxPoints[blobNr-1]
            for rowIndex in range(startRow, endRow):
                
                if rowIndex in [startRow, endRow-1]:
                    colRange = range(startCol, endCol)
                else:
                    colRange = [startCol, endCol-1]
                for colIndex in colRange:
                    scale = np.ceil(200/len(boxPoints))-1
                    image[rowIndex][colIndex] = scale*blobNr
        cv2.imshow("Bobo", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return boxPoints

def cropBoundingBoxes(boxPoints, image):
    # find every point in between the boxpoints and put these points into a list/array/whatever
    minRowCoorBox = []
    minColCoorBox = []
    maxRowCoorBox = []
    maxColCoorBox = []
    for blobindex in range(len(boxPoints)):
        minRowCoorBox.append(boxPoints[blobindex][0][0])
        minColCoorBox.append(boxPoints[blobindex][0][1])
        maxRowCoorBox.append(boxPoints[blobindex][1][0])
        maxColCoorBox.append(boxPoints[blobindex][1][1])

    allCroppedImages = []
    for blobindex in range(len(minColCoorBox)):
        croppedImage = []
        # for loop over the minimum to maximum coordinate of the rows
        for ii in range(minRowCoorBox[blobindex], maxRowCoorBox[blobindex]+1):
            croppedImage.append((image[ii][minColCoorBox[blobindex]: maxColCoorBox[blobindex]+1]))
        allCroppedImages.append(croppedImage)


    return allCroppedImages


def saveCroppedImages(filename, allCroppedImages, path):
    # save new mat objects to github folder and name each new image like classname_number
    classname = filename.split(".")[0]

    for blobindex in range(len(allCroppedImages)):
        filename = "%s_%d.jpg" % (classname, blobindex+1)
        image = np.uint8(allCroppedImages[blobindex])
        cv2.imwrite(path+filename, image)

    return 0
