import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage.feature import hog
from skimage import data, exposure
import retrieveFeaturesSim as featSim

imageWD = 'C:\Visionplaatje\\'
filename = 'drie.jpg'
imagePath = imageWD + filename
img = cv2.imread(imagePath)

if img.any() == None:
    print "Error. Could not read file."
else:
    print "De imagefile = " + filename

cv2.imshow("orgineel", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow("gray", grayImage)
cv2.waitKey(0)
cv2.destroyAllWindows()

hogImage = featSim.retrieveHOG(grayImage)
cv2.imshow("hog", hogImage)
cv2.waitKey(0)
cv2.destroyAllWindows()