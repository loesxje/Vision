from IPython import get_ipython
ipython = get_ipython()

ipython.magic('reset -sf')

from skimage import measure
import numpy as np
import cv2
import avansvisionlibSim as avl
import sys
from skimage import draw


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

grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

grayImage = cv2.GaussianBlur(grayImage, (9,9),0.)

binaryImage = cv2.threshold(grayImage, 240, 1, cv2.THRESH_BINARY_INV)[1]

avl.show16SImageStretch(binaryImage, "Binary Image")
cv2.destroyAllWindows()
  

labeledImage = measure.label(binaryImage, background=0)
totalBlobs = np.max(labeledImage)
labeledImage = np.uint8(labeledImage)


avl.show16SImageStretch(labeledImage, "show Blobs")
cv2.destroyAllWindows()
print totalBlobs

[contourImage, contourVec] = avl.makeContourImage(binaryImage)
            
avl.show16SImageStretch(contourImage, "show Contour")
cv2.destroyAllWindows()