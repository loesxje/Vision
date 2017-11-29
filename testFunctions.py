import numpy as np
import matplotlib as mplot
import avansvisionlibLOES as avl
import cv2

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

avl.show16SImageStretch(testMatrix, "binimg")
cv2.destroyAllWindows()