HAHA JULLIE KUNNEN GEEN RTF INLEZEN
Veranderen:

In ExtractFeatures.py:

def outputToNumber(OO):
    OO.resize(1,len(OO))
    if (sum(sum(OO == np.array([0,0,0,0])))) == 4:
        numberRecognized = 0
    elif (sum(sum(OO == np.array([0,0,0,1])))) == 4:
        numberRecognized = 1
    elif (sum(sum(OO == np.array([0,0,1,0])))) == 4:
        numberRecognized = 2
    elif (sum(sum(OO == np.array([0,0,1,1])))) == 4:
        numberRecognized = 3
    elif (sum(sum(OO == np.array([0,1,0,0])))) == 4:
        numberRecognized = 4
    elif (sum(sum(OO == np.array([0,1,0,1])))) == 4:
        numberRecognized = 5
    elif (sum(sum(OO == np.array([0,1,1,0])))) == 4:
        numberRecognized = 6
    elif (sum(sum(OO == np.array([0,1,1,1])))) == 4:
        numberRecognized = 7
    elif (sum(sum(OO == np.array([1,0,0,0])))) == 4:
        numberRecognized = 8
    elif (sum(sum(OO == np.array([1,0,0,1])))) == 4:
        numberRecognized = 9
    else:
        print("Could not correctly classify object.")
    return numberRecognized

Toevoegen:
In testProgramma.py:
aan het begin van testHandwrittenNumbers, om de imageCodes gesorteerd op nummer in te lezen (gaat nu van 1 naar 10 naar 11 ipv 1 2 3)
de line print(confusionMatrix) onderaan in testHandwrittenNumbers
De gehele definitie confusionMatrix
import re

def testHandwrittenNumbers(imageWD, V0, W0):
    imageCodes = []

    for file in os.listdir(imageWD):  # +folder
        if file != ".DS_Store":
            imageCodes.append(file)

    print(imageCodes)

    perimeterMax, areaMax = ef.memoriseLargest(imageWD)
    OOlist = []

    for i in range(len(imageCodes)):
        indexnummer = np.random.randint(len(imageCodes))
        filename = imageCodes.pop(indexnummer)
        print(filename)
		filenameList.append(filename)
        image = cv2.imread(imageWD + filename)
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        binaryImage = cv2.threshold(grayImage, 140, 1, cv2.THRESH_BINARY_INV)[1]
        IT = np.array(ef.extractFeatures(binaryImage,perimeterMax, areaMax))
        OO = np.array(BPN.BPN(IT,V0,W0))
        OO = np.round(np.round(OO,1))
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

    #realOutput = ["five", "nine", "one", "four", "two", "six", "three", "one", "nine", "eight","seven", "five", "nine", "three", "three", "five", "six", "two", "three", "two", "six", "four", "eight", "four", "eight", "three", "five", "two", "nine", "three", "three", "seven", "zero", two", "nine" "eight", "eight", "four", "seven", "one"] #alle 40 de images
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
