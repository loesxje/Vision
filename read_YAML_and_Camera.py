import numpy as np
import matplotlib as mplot
import yaml
import cv2

doCallibrate = False

if doCallibrate:
    # read YML file.
    with open("ueyecallib.yml", 'r') as stream:
        try:
            print(yaml.load(stream))
        except yaml.YAMLError as exc:
            print(exc)

# read camera images
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        raise ValueError("Failed to load frames")
    # Our operations on the frame come here
    grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv2. imshow('frame', grayImage)
    key = cv2.waitKey(1) # Break when spacebar is pressed
    if key == 32:
        break

cv2.imwrite("frameSaveTest.jpg", grayImage)

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()