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
    #argument contourvector comes from makeContourImage

    #for i in size(findNextBlob):
        #calc min_x & min_y from the contour of every Blob
        #calc max_x & max_y from the contour of every Blob
    bbs = []

    for i in range(len(contourvector)):
        bbox = BoundingBox(contourvector[i])
        bbs.append([(bbox._min[0], bbox._min[1]), (bbox._max[0], bbox._max[1])])
    return bbs

def biggestBoundingBox(bounding_boxes_vector):
    #calc difference min_x & max_x & min_y & max_y
    row_difference = 0
    col_difference = 0
    for i in range(len(bounding_boxes_vector)):
        row_dif = bounding_boxes_vector[i][1][0] - bounding_boxes_vector[i][0][0]
        col_dif = bounding_boxes_vector[i][1][1] - bounding_boxes_vector[i][0][1]
        if(row_dif > row_difference):
            row_difference = row_dif
        if(col_dif > col_difference):
            col_difference = col_dif

    #make the length of the biggest bounding box odd. This way, it is easier to define a middle
    if(row_difference%2 == 0):
        row_difference += 1
    if(col_difference%2 == 0):
        col_difference += 1

    #save greatest difference x & y
    biggestbb = [row_difference, col_difference]

    return biggestbb

def getCoordinatesAllBoundingBoxes(all_bounding_boxes, biggest_bounding_box, image):
    #draw boxes
        #all points in between
            #(min_x, min_y) (min_x, max_y)
            #(min_x, max_y) (max_x, max_y)
            #(max_x, max_y) (max_x, min_y)
            #(max_x, min_y) (min_x, min_y)

    #start in the middle of the Blob
    middle = []

    for i in range(len(all_bounding_boxes)):
        max_row = all_bounding_boxes[i][1][0]
        min_row = all_bounding_boxes[i][0][0]

        max_col = all_bounding_boxes[i][1][1]
        min_col = all_bounding_boxes[i][0][1]
        middle.append([(((max_row - min_row) / 2) + min_row), (((max_col - min_col) / 2) + min_col)])

    #find boxpoints per blob that exist within the imagesize
    box_points = []
    for i in range(len(all_bounding_boxes)):
        start_box_up_down = middle[i][0] - 0.5 * biggest_bounding_box[1]
        end_box_up_down = middle[i][0] + 0.5 * biggest_bounding_box[1]

        if(start_box_up_down < 0):
            end_box_up_down -= start_box_up_down
            start_box_up_down = 0
        elif(end_box_up_down > image.shape[1]):
            start_box_up_down -= end_box_up_down
            end_box_up_down = image.shape[1]

        start_box_left_right = middle[i][1] - 0.5 * biggest_bounding_box[0]
        end_box_left_right = middle[i][1] + 0.5 * biggest_bounding_box[0]

        if(start_box_left_right < 0):
            end_box_left_right -= start_box_left_right
            start_box_left_right = 0
        elif(end_box_left_right > image.shape[0]):
            start_box_left_right -= end_box_left_right
            end_box_left_right = image.shape[0]

        box_points.append([[start_box_left_right, start_box_up_down], [start_box_left_right, end_box_up_down], [end_box_left_right, end_box_up_down], [end_box_left_right, start_box_up_down]])


                #for j in range(difference_x):
                    #line_up.append(start_draw_up_down + 0.5*difference_y)
                    #line_down.append(start_draw_up_down - 0.5*difference_y)
                    #start_draw_up_down += j

                # start_draw_left_right = middle_blob - 0.5*difference_y
                # for k in range(difference_y):
                    # line_left.append(start_draw_left_right + 0.5*difference_x)
                    # line_right.append(start_draw_left_right + 0.5*difference_x)
                    # start_draw_left_right += k
    return box_points
        #draw lines


