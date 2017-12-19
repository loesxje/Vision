from IPython import get_ipython
ipython = get_ipython()

#ipython.magic('reset -sf')

from skimage import measure
import numpy as np
import cv2
import avansvisionlib as avl
import sys
import TESTSIMboundingBoxes as bobo
import retrieveFeaturesSim as retFeat
# =============================================================================
showImages = True
doGauss = True
doClose = True
doThicken = True
doContrast = True
# =============================================================================

# ==============GEEF HIER JE PLAATJE EN BIJBEHORENDE PAD=======================
imageWD = 'C:\Visionplaatje\\numbers\\train\\'
filename = 'eight_1.jpg'
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

if doContrast:
    hist,bins = np.histogram(grayImage.flatten(),256,[0,256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max()/ cdf.max()
    cdf_m = np.ma.masked_equal(cdf,0)
    cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
    cdf = np.ma.filled(cdf_m,0).astype('uint8')
    grayImage = cdf[grayImage]
[hogImage, hogVector] = retFeat.retrieveHOG(grayImage, True)
# =============================================================================
# 
# if showImages:
#     # Show original image
#     cv2.imshow("Gray Image", grayImage)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     
# # Pre process the image
# binaryImage = cv2.threshold(grayImage, 160, 1, cv2.THRESH_BINARY_INV)[1]
# if doGauss:
#     binaryImage = cv2.GaussianBlur(binaryImage, (5,5), 0.)
# if doClose:
#     binaryImage = cv2.morphologyEx(binaryImage, cv2.MORPH_CLOSE, kernel = np.ones([5,5]))
# if doThicken:
#     binaryImage = cv2.dilate(binaryImage, (5,5), 4)
# 
# 
# if showImages:
#     avl.show16SImageStretch(binaryImage, "Binary Image")
#     cv2.destroyAllWindows()
#   
# # label BLOBs and determine the number of blobs
# labeledImage = measure.label(binaryImage, background=0)
# totalBlobs = np.max(labeledImage)
# labeledImage = np.uint8(labeledImage) #convert to uint8. Otherwise the picture
# # can't be shown
# 
# if showImages:
#     avl.show16SImageStretch(labeledImage, "show Blobs")
#     cv2.destroyAllWindows()
# 
# print "Total Blobs = " + str(totalBlobs)
# 
# # retrieve BLOBs contours
# # OUT:
# #   contourImage is the image with the contours
# #   contourVec is a vector with the coordinates of the contours
# 
# [aantal, contourImage, contourVec] = avl.allContours(binaryImage) 
# 
# if showImages:            
#     avl.show16SImageStretch(contourImage, "show Contour")
#     cv2.destroyAllWindows()
# 
# boBos = bobo.allBoundingBoxes(contourVec)
# bigBoBo = bobo.biggestBoundingBox(boBos)
# boxPoints = bobo.getCoordinatesAllBoundingBoxes(boBos, bigBoBo, img, showImages)
# 
# fillContour = avl.contourFourConnected(contourImage, labeledImage)
# 
# =============================================================================
