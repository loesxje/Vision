import numpy as np
import cv2
from planar import BoundingBox


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
        bbox = BoundingBox(contourvector[i])
        minCor = (bbox._min[0], bbox._min[1]) #tuple(minRow, minCol)
        maxCor = (bbox._max[0], bbox._max[1]) #tuple(maxRow, maxCol)
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
    
    #draw boxes
        #all points in between
            #(min_x, min_y) (min_x, max_y)
            #(min_x, max_y) (max_x, max_y)
            #(max_x, max_y) (max_x, min_y)
            #(max_x, min_y) (min_x, min_y)

    #start in the middle of the Blob
    middle = []

    for i in range(len(allBoBo)):
        maxRow = allBoBo[i][1][0]
        minRow = allBoBo[i][0][0]

        maxCol = allBoBo[i][1][1]
        minCol = allBoBo[i][0][1]
        
        midRow = (((maxRow - minRow) / 2) + minRow)
        midCol = (((maxCol - minCol) / 2) + minCol)
        middle.append([midRow, midCol])

    #find boxpoints per blob that exist within the imagesize
    boxPoints = []
    for i in range(len(allBoBo)):
        startRow= int(np.ceil(middle[i][0] - 0.5 * biggestBoBo[0]))
        endRow = int(np.ceil(middle[i][0] + 0.5 * biggestBoBo[0]))

        if(startRow < 0):
            endRow += startRow * -1 # negative * -1 = positive
            startRow = 0
        elif(endRow > image.shape[0]):
            startRow += int(np.ceil(image.shape[0])) + endRow 
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
            #for j in range(difference_x):
                    #line_up.append(start_draw_up_down + 0.5*difference_y)
                    #line_down.append(start_draw_up_down - 0.5*difference_y)
                    #start_draw_up_down += j

                # start_draw_left_right = middle_blob - 0.5*difference_y
                # for k in range(difference_y):
                    # line_left.append(start_draw_left_right + 0.5*difference_x)
                    # line_right.append(start_draw_left_right + 0.5*difference_x)
                    # start_draw_left_right += k
    return boxPoints
        #draw lines
