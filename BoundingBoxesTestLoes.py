import numpy as np
import cv2
import matplotlib.pyplot as plt
from planar import BoundingBox

#Make bounding boxes

#func:  delivers bounding boxes of def contours
#pre:   def contours contains the contours for which bounding boxes have to be delivered
#post:  bbs contains all bounding boxes. The index corresponds to the index of contours.
#           i.e. bbs[i] belongs to contours[i]

def allBoundingBoxes(contourvector):
    #argument contourvector comes from findContours

    #for i in size(findNextBlob):
        #calc min_x & min_y from the contour of every Blob
        #calc max_x & max_y from the contour of every Blob
    bbs = []

    for i in range(len(contourvector)):
        bbox = BoundingBox(contourvector[i])
        bbs.append([(bbox._min[0], bbox._min[1]), (bbox._max[0], bbox._max[1])])
    print(bbs)

    #calc difference min_x & max_x & min_y & max_y
    #save greatest difference x & y

    #draw boxes
        #all points in between
            #(min_x, min_y) (min_x, max_y)
            #(min_x, max_y) (max_x, max_y)
            #(max_x, max_y) (max_x, min_y)
            #(max_x, min_y) (min_x, min_y)
        #start in down left or in the middle of the Blob?
            # middle: start at the middle_blob

        #calc boxes per blob
            # middle_Blob = ergens uit labelBLOBsInfo
            # for i in range(size(findNextBlob)):
                #start_draw_up_down = middle_blob - 0.5*difference_x
                #for j in range(difference_x):
                    #line_up.append(start_draw_up_down + 0.5*difference_y)
                    #line_down.append(start_draw_up_down - 0.5*difference_y)
                    #start_draw_up_down += j

                # start_draw_left_right = middle_blob - 0.5*difference_y
                # for k in range(difference_y):
                    # line_left.append(start_draw_left_right + 0.5*difference_x)
                    # line_right.append(start_draw_left_right + 0.5*difference_x)
                    # start_draw_left_right += k

        #draw lines




