import numpy as np
import cv2
import avansvisionlibSim as avl

imageWD = 'C:\Visionplaatje\\'
filename = 'testImg.png'
imagePath = imageWD + filename
img = cv2.imread(imagePath)

if img.any() == None:
    print "Error. Could not read file."
else:
    print "De imagefile = " + filename

grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

binaryImage = cv2.threshold(grayImage, 180, 1, cv2.THRESH_BINARY_INV)[1]
avl.printMatrix(binaryImage)

avl.show16SImageStretch(binaryImage, "Binary Image")
cv2.destroyAllWindows()
testMatrix = avl.makeAdmin(binaryImage)
avl.printMatrix(testMatrix)

for ii in range(8):
    if avl.getEntryNeighbour(testMatrix, 3,3,ii) == -1:
        print ii
        break
    

    