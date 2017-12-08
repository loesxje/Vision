import numpy as np
import cv2

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


def saveCroppedImages(filename, allCroppedImages):
    # save new mat objects to github folder and name each new image like classname_number
    classname = filename.split(".")[0]

    for blobindex in range(len(allCroppedImages)):
        sprintf(filename, "%d_%d.jpg", classname, blobindex+1)
        image = np.uint8(allCroppedImages[blobindex])
        #imwrite(filename, image)

    return 0