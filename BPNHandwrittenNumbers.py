import cv2
import numpy as np
import avlBPNEvaWorking as BPN
import avansvisionlib as avl
import pandas as pd
import os
import extractFeatures as ef

# =================== GEEF HIER HET BIJBEHORENDE PAD OP =======================
imageWD = '/Users/Eva/Workspace_programs/PycharmProjects/Vision-master/Afbeeldingen//'
# =============================================================================

# Maximale fout die toegestaan wordt in de output voor de training input
MAX_OUTPUT_ERROR = 1E-10
# maximaal aantal runs dat uitgevoerd wordt bij het trainen
MAXRUNS = 10000

outputError0 = MAX_OUTPUT_ERROR + 1
outputError1 = MAX_OUTPUT_ERROR + 1
sumSqrDiffError = MAX_OUTPUT_ERROR + 1

for file in os.listdir(imageWD): #+folder
    if file != ".DS_Store":
        numberOfInputs = len(os.listdir(imageWD))

#TODO: HARDCODED?
numberOfFeatures = 5
numberOfOutputs = 4

print("\n Testset laden... \n \n")
print("\t BPN Inputlayer  = " + str(numberOfInputs) + " neurons")
print("\t BPN Outputlayer = " + str(numberOfOutputs) + " neurons")
hiddenNeurons  = int(input("Please choose a number of hidden neurons: "))
print("Thank You!!")

print("Initialize BPN... ")

V0, W0, dV0, dW0 = BPN.initializeBPN(numberOfFeatures, hiddenNeurons, numberOfOutputs)
inputList = []
outputList = []
imageCodes = []

#Haal de afbeeldingen uit de map.
for file in os.listdir(imageWD): # +folder
    if file != ".DS_Store":
        imageCodes.append(file)
        print(imageCodes)
        for i in range(len(imageCodes)):
            indexnummer = np.random.randint(len(imageCodes))
            filename = imageCodes.pop(indexnummer)
            print(filename)
            image = cv2.imread(imageWD + filename)
            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            #TODO: is de Gaussian Blur nog nodig?
            blurredImage = cv2.GaussianBlur(grayImage, (5, 5), 0)
            binaryImage = cv2.threshold(blurredImage, 140, 1, cv2.THRESH_BINARY_INV)[1]

            runs = 0

            outputError0 = MAX_OUTPUT_ERROR + 1
            outputError1 = MAX_OUTPUT_ERROR + 1
            sumSqrDiffError = MAX_OUTPUT_ERROR + 1
            # looping over afbeeldingen met eenen,tweeen drieen, vieren, vijfen, zessen enz
            # Voor elke feature worden de weights bepaald

            while ((sumSqrDiffError > MAX_OUTPUT_ERROR) & (runs < MAXRUNS)):
                sumSqrDiffError = 0
            #     for inputSetRowNr in range(ITset.shape[0]):  # Afbeeldingen in de map
                #for inputSetRowNr in range(binaryImage.shape[0]):
                IT = np.array(ef.extractFeatures(binaryImage))
                OT = np.array(ef.outputHandwrittenNumbers(file))
                OH = BPN.calculateOutputHiddenLayer(IT, V0)
                OO = BPN.calculateOutputBPN(OH, W0)
                [V1, W1] = BPN.adaptVW(OT, OO, OH, IT, W0, dW0, V0, dV0)
                outputError0 = BPN.calculateOutputBPNError(OO, OT)
                outputError1 = BPN.calculateOutputBPNError(BPN.BPN(IT, V1, W1), OT)
                sumSqrDiffError += (outputError1 - outputError0) * (outputError1 - outputError0)
                V0 = V1
                W0 = W1
                print("sumSqrDiffError = " + str(sumSqrDiffError))
                runs += 1
            inputList.append([IT])
            outputList.append([OT])
        #
#Print de output
# outputVectorBPN = OTset.copy()
# for inputSetRowNr in range(ITset.shape[0]):
#     for inputSetColNr in range(OTset.shape[1]):
#         inputVectorTrainingSet = ITset[inputSetRowNr]
#         outputVectorBPN[inputSetRowNr][inputSetColNr] = round(round(BPN.BPN(inputVectorTrainingSet, V0, W0)[inputSetColNr][0]), 1)
#
print("BPN Training is ready!")
print("Runs = " + str(runs))
# outputTraining = pd.DataFrame(outputVectorBPN)
# outputTraining.columns = ["Output BPN"]
# originalSet[outputTraining.columns] = outputTraining
# print(originalSet)


# ========================= TEST DE WEGINGSFACTOREN ===========================
# IT = np.array(ef.extractFeatures(binaryImage))
# IT * V0 = IH
# =============================================================================
