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
cap = cv2.VideoCapture(1)
print cap.isOpened()
for ii in range(10):

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            cap.release()
            cv2.destroyAllWindows()
            raise ValueError("Failed to load frames")
        # Our operations on the frame come here
        grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Display the resulting frame
        cv2. imshow('frame', grayImage)
        key = cv2.waitKey(1) # Break when spacebar is pressed
        if key == 32:
            break

    # name = raw_input("train or test? ")
    # if name == "train":
    #     number = raw_input("What number?" )
    #     cv2.imwrite("C:/VisionPlaatje/CameraCaps/{}{}.jpg".format(name, number), grayImage)
    # elif name == "stop":
    #     break
    # else:
    #     cv2.imwrite("C:/VisionPlaatje/CameraCaps/{}.jpg".format(name), grayImage)

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()