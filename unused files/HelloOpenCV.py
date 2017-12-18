import cv2

imageWD = 'C:\Visionplaatje\\'
filename = 'rummikub0.jpg'
imagePath = imageWD + filename
img = cv2.imread(imagePath)

if img.any() == None:
    print "Error. Could not read file."
else:
    print "De imagefile = " + filename

cv2.imshow("Monsters", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow("Gray Monsters", grayImage)
cv2.waitKey(0)
cv2.destroyAllWindows()


