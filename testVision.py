import numpy as np
import cv2
import avansvisionlibSim as avl

imageWD = 'C:\Visionplaatje\\'
filename = 'monsters.jpg'
imagePath = imageWD + filename
img = cv2.imread(imagePath)

if img.any() == None:
    print "Error. Could not read file."
else:
    print "De imagefile = " + filename

grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

binaryImage = cv2.threshold(grayImage, 165, 1, cv2.THRESH_BINARY_INV)[1]
avl.printMatrix(binaryImage)

avl.show16SImageStretch(binaryImage, "Binary Image")
cv2.destroyAllWindows()
  
[totalBlobs, labeledImage] = avl.labelBLOBs(binaryImage)
avl.show16SImageStretch(labeledImage, "show Blobs")
cv2.destroyAllWindows()
print totalBlobs