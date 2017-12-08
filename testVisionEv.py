from skimage import measure
import numpy as np
import cv2
import avansvisionlibSim as avl
import sys
import algorithmsEVa as algo

from skimage import draw
import boundingBoxesEva as eva

# ==============GEEF HIER JE PLAATJE EN BIJBEHORENDE PAD=======================
imageWD = '/Users/Eva/Workspace_programs/CLionProjects/Visiongev//'
filename = 'monsters.jpg'
# =============================================================================

# lOAD IMAGE
imagePath = imageWD + filename
img = cv2.imread(imagePath)

# check if image loaded correctly
if type(img) == type(None):
    sys.exit("Error. Could not read file.")
else:
    print("De imagefile = " + filename)

grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

binaryImage = cv2.threshold(grayImage, 240, 1, cv2.THRESH_BINARY_INV)[1]
avl.show16SImageStretch(binaryImage, "Binary Image")
cv2.destroyAllWindows()

labeledImage = measure.label(binaryImage, background=0)
totalBlobs = np.max(labeledImage)
labeledImage = np.uint8(labeledImage)

avl.show16SImageStretch(labeledImage, "show Blobs")
cv2.destroyAllWindows()

contourImage = algo.makeContourImage(binaryImage)
print("Totaal aantal blobs is \t", totalBlobs)

firstPixel = algo.findFirstPoint(binaryImage, 1.)

contours = algo.getContourList(contourImage)
region = []

for contour in contours:
    regionPixel = algo.enclosedPixels(contour, contourImage, binaryImage, region)
    region.append(regionPixel)

floodFillImage = binaryImage.copy()
floodFillImage = 0
for vector in regionPixels:
    for i in vector:
        floodFillImage[i[0], i[1]] = 255

cv2.imshow("Flood Filled",floodFillImage)
cv2.destroyAllWindows()