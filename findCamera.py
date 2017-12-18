import cv2
from pyueye import ueye

print("Search for camera...")
cameraId = []
for ii in range(0, 100000000):
    cap = cv2.VideoCapture(ii)
    if cap.isOpened():
        print "Camera found on port {}".format(ii)
        cameraId.append(ii)
# =============================================================================
#         # Our operations on the frame come here
#         grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# =============================================================================
        
    cap.release()
    if ii%50000 == 0:
        print ii


# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()