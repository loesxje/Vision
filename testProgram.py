import cv2
import numpy as np
import avlBPNEvaWorking as BPN
import avansvisionlib as avl
import pandas as pd
import os
import extractFeatures as ef
import re

def testHandwrittenNumbers(imageWD, V0, W0):
    imageCodes = []

    for file in os.listdir(imageWD):  # +folder
        if file != ".DS_Store":
            numberOfInputs = len(os.listdir(imageWD))
            imageCodes.append(file)

    print(imageCodes)
    OOlist = []
    filenameList = []

    for i in range(len(imageCodes)):
        indexnummer = np.random.randint(len(imageCodes))
        filename = imageCodes.pop(indexnummer)
        filenameList.append(filename)
        binaryImage = ef.makeBinaryImage(imageWD + filename)
        IT = np.array(ef.extractFeatures(binaryImage))
        OOraw = np.array(BPN.BPN(IT,V0,W0))
        OO = np.array(BPN.BPN(IT, V0, W0))
        OO = np.round(np.round(OO,1))
        print(OOraw)
        OOlist.append(OO)
    print(confusionMatrix(OOlist, filenameList))


def confusionMatrix(OOlist, filenameList):
    numberOutput = []
    for i in range(len(OOlist)):
        OOnumber = ef.outputToNumber(OOlist[i])
        numberOutput.append(OOnumber)

    combinedList = []
    for i in range(len(filenameList)):
        combinedList.append([filenameList[i], numberOutput[i]])

    filenameList.sort(key=lambda var: [int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])

    newCombinedList = []
    outputTest = []
    for files in filenameList:
        for i in range(len(filenameList)):
            if files == combinedList[i][0]:
                newCombinedList.append(combinedList[i])
                outputTest.append(combinedList[i][1])

    #realOutput = ["five", "nine", "one", "four", "two", "six", "three", "one", "nine", "eight","seven", "five", "nine", "three", "three", "five", "six", "two", "three", "two", "six", "four", "eight", "four", "eight", "three", "five", "two", "nine", "three", "three", "seven", "zero", two", "nine" "eight", "eight", "four", "seven", "one"] #alle 20 de images
    realOutput = [5,9,1,4,2,6,3,1,9,8]

    confusionMat = np.zeros((len(outputTest),len(realOutput)))

    for i in range(len(realOutput)):
        confusionMat[realOutput[i],outputTest[i]] += 1

    accuracy = []
    confusionDiagonal = confusionMat.diagonal()
    for i in range(len(outputTest)):
        if sum(confusionMat[i]) == 0:
            accuracyPerRow = 0
        else:
            accuracyPerRow = confusionDiagonal[i]/(sum(confusionMat[i]))
        accuracy.append(accuracyPerRow)

    confusiondf = pd.DataFrame(confusionMat)
    accuracydf = pd.DataFrame(accuracy)
    accuracydf.columns = ["Accuracy"]
    confusiondf[accuracydf.columns] = accuracydf

    return confusiondf
