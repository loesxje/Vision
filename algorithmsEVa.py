import numpy as np
import cv2
from skimage import measure

def makeContourImage(binaryImage):
    # contours = measure.find_contours(binaryImage, level = 0., fully_connected = "low",positive_orientation = "low")
    (image2, contours, onzin) = cv2.findContours(binaryImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contourImage = np.zeros(np.shape(binaryImage))
    for ii in range(len(contours)):
        numCor = len(contours[ii])
        corIndex = range(numCor)
        for cor in contours[ii][corIndex]:
            row = cor[0][0]
            col = cor[0][1]
            contourImage[col][row] = 1

    return contourImage

def findFirstPoint(inputImage, pixelValue):
    rowsize = inputImage.shape[0]
    colsize = inputImage.shape[1]
    labeledImage = measure.label(inputImage, background=0)
    totalBlobs = np.max(labeledImage)
    labeledImage = np.uint8(labeledImage)

    firstPoint = []
    for blob in range(1, totalBlobs):
        firstFoundBool = False
        for rows in range(rowsize):
            for cols in range(colsize):
                if (inputImage[rows, cols] == pixelValue) & (labeledImage[rows, cols] == blob):
                    firstPoint.append([rows, cols])
                    firstFoundBool = True
                if firstFoundBool == True:
                    break
            if firstFoundBool == True:
                break
    return firstPoint

def getContourList(contourImage):
    contours = []
    rowsize = contourImage.shape[0]
    colsize = contourImage.shape[1]

    for rows in range(rowsize):
        for cols in range(colsize):
            if (contourImage[rows, cols] == 1):
                contours.append([rows, cols])
    return contours

def floodFill(edge,floodFillImage,pixelValue):
    rowEdge = []
    colEdge = []
    for i in range(len(edge)):
        rowEdge.append(edge[i][0])
        colEdge.append(edge[i][1])
        for j in range(len(rowEdge)):
            floodFillImage[rowEdge[j], colEdge[j]] = pixelValue

def makeFloodFillImage(contourImage, binaryImage):
    boundaryImage = contourImage.copy()
    rowsize = contourImage.shape[0]
    colsize = contourImage.shape[1]

    for rows in range(rowsize):
        for cols in range(colsize):
            if contourImage[rows, cols] == 1:
                boundaryImage[rows, cols] = 101

    return boundaryImage - binaryImage

def enclosedPixels(contour, contourImage, binaryImage, region):

    chainCoordinate = [[-1,-1],[1,1]]

    floodFillImage = makeFloodFillImage(contourImage, binaryImage)
    firstInteriorPoint = findFirstPoint(floodFillImage, -1.)
    region = firstInteriorPoint
    edge = firstInteriorPoint

    newEdge = []

    while len(edge) > 0:
        for regionPoint in region:
            if regionPoint != region:
                for edges in edge:
                    if (contour != [edges[0] + chainCoordinate[0][0], edges[1]]) & (regionPoint != [edges[0] + chainCoordinate[0][0], edges[1]]):
                        if (newEdge != [edges[0] + chainCoordinate[0][0], edges[1]]) & (floodFillImage[edges[0] + chainCoordinate[0][0], edges[1]] == -1.):
                            newEdge.append([edges[0] + chainCoordinate[0][0], edges[1]])

                    if (contour != [edges[0], edges[1] + chainCoordinate[0][1]]) & (regionPoint != [edges[0], edges[1] + chainCoordinate[0][1]]):
                        if (newEdge != [edges[0], edges[1] + chainCoordinate[0][1]]) & (floodFillImage[edges[0], edges[1] + chainCoordinate[0][1]] == -1.):
                            newEdge.append([edges[0], edges[1] + chainCoordinate[0][1]])

                    if (contour != [edges[0] + chainCoordinate[1][0], edges[1]]) & (regionPoint != [edges[0] + chainCoordinate[1][0], edges[1]]):
                        if (newEdge != [edges[0] + chainCoordinate[1][0], edges[1]]) & (floodFillImage[edges[0] + chainCoordinate[1][0], edges[1]] == -1.):
                            newEdge.append([edges[0] + chainCoordinate[1][0], edges[1]])

                    if (contour != [edges[0] ,edges[1]+ chainCoordinate[1][1]]) & (regionPoint != [edges[0] ,edges[1]+ chainCoordinate[1][1]]):
                        if (newEdge != [edges[0] ,edges[1]+ chainCoordinate[1][1]]) & (floodFillImage[edges[0] ,edges[1]+ chainCoordinate[1][1]] == -1.):
                            newEdge.append([edges[0] ,edges[1]+ chainCoordinate[1][1]])


                edge = newEdge
                region[:0] = newEdge
                newEdge = []

    return region