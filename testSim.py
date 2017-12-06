from IPython import get_ipython
ipython = get_ipython()

#ipython.magic('reset -sf')

from skimage import measure
import numpy as np
import cv2
import avansvisionlib as avl
import sys

# =================BEPAAL OF JE AFBEELDINGEN WIL ZIEN==========================
showImages = False
# =============================================================================

# ==============GEEF HIER JE PLAATJE EN BIJBEHORENDE PAD=======================
imageWD = 'C:\Visionplaatje\\'
filename = 'monsters.jpg'
# =============================================================================

# lOAD IMAGE
imagePath = imageWD + filename
img = cv2.imread(imagePath)

# check if image loaded correctly
if type(img) == type(None):
    sys.exit("Error. Could not read file.")
else:
    print "De imagefile = " + filename

if showImages:
    # Show original image
    cv2.imshow("Original", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Convert original to grayscale
grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Pre process the image
binaryImage = cv2.threshold(grayImage, 240, 1, cv2.THRESH_BINARY_INV)[1]
binaryImage = cv2.GaussianBlur(binaryImage, (17,17), 0.)
binaryImage = cv2.morphologyEx(binaryImage, cv2.MORPH_CLOSE, kernel = np.ones([3,3]))

if showImages:
    avl.show16SImageStretch(binaryImage, "Binary Image")
    cv2.destroyAllWindows()
  
# label BLOBs and determine the number of blobs
labeledImage = measure.label(binaryImage, background=0)
totalBlobs = np.max(labeledImage)
labeledImage = np.uint8(labeledImage) #convert to uint8. Otherwise the picture
# can't be shown

if showImages:
    avl.show16SImageStretch(labeledImage, "show Blobs")
    cv2.destroyAllWindows()

print "Total Blobs = " + str(totalBlobs)

# retrieve BLOBs contours
# OUT:
#   contourImage is the image with the contours
#   contourVec is a vector with the coordinates of the contours
[contourImage, contourVec] = avl.makeContourImage(binaryImage) 

if showImages:            
    avl.show16SImageStretch(contourImage, "show Contour")
    cv2.destroyAllWindows()