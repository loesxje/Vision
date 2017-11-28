import numpy as np
import matplotlib as mplot


def labelIter(admin, blobNr):
    x = row
    y = col
    admin[x][y] = blobNr * 10 + 8

    next1 = -999
    area = 1

    allLabeledFlag = True
    while (allLabeledFlag):
        allLabeledFlag = False
        pathLabeled = False
        while not (pathLabeled):
            if (not allLabeledFlag):
                allLabeledFlag = moreNext1(admin, x, y)
                findNext1(admin, x, y, next1)

            if (next1 >= 0):
                admin[x][y] = blobNr * 10 + next1
                area += area

            else:
                findPrevious = admin[x][y] #% 10
                print findPrevious
                if (findPrevious = 0):
                    x += 1
                    break
                ifelse(findPrevious = 1):
                x += 1
                y -= 1
                break
                ifelse(findPrevious = 2):
                y -= 1
                break;
                ifelse(findPrevious = 3):
                x -= 1
                y -= 1
                break
                ifelse(findPrevious = 4):
                x -= 1
                break
                ifelse(findPrevious = 5):
                x -= 1
                y += 1
                break
                ifelse(findPrevious = 6):
                y += 1
                break
                ifelse(findPrevious = 7):
                x += 1
                y += 1
                ifelse(pathLabeled = True):
                break
                else:
                print "Error func labelIter!"
    return area

a = np.array([[0,0,0], [-1,0,0], [0,0,-1]])
labelIter(a,1)