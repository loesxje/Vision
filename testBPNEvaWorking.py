import cv2
import numpy as np
import avlBPN as BPN
import avansvisionlibSim as avl
import pandas as pd

# Maximale fout die toegestaan wordt in de output voor de training input
MAX_OUTPUT_ERROR = 1E-10
# maximaal aantal runs dat uitgevoerd wordt bij het trainen
MAXRUNS = 10000


print("\n Testset laden... \n \n")

ITset, OTset = BPN.loadTrainingXOR()

originalSet = pd.DataFrame(ITset)
originalSet.columns = ["I0", "I1"]
outputSet = pd.DataFrame(OTset)
outputSet.columns = ["Expected Output"]
originalSet[outputSet.columns] = outputSet
print(originalSet)

print("BPN format: ")
print("\t BPN Inputlayer  = " + str(ITset.shape[1]) + " neurons")
print("\t BPN Outputlayer = " + str(OTset.shape[1]) + " neurons")
hiddenNeurons  = int(input("Please choose a number of hidden neurons: "))
print("Thank You!!")

print("Initialize BPN... ")

V0, W0, dV0, dW0 = BPN.initializeBPN(ITset.shape[1], hiddenNeurons, OTset.shape[1]);

print("initial values of weight matrices V0 and W0 \n*******************************************")
avl.printMatrix(V0)
avl.printMatrix(W0)

input("===> PRESS ENTER")

outputError0 = MAX_OUTPUT_ERROR + 1
outputError1 = MAX_OUTPUT_ERROR + 1
sumSqrDiffError = MAX_OUTPUT_ERROR + 1

runs = 0

while ((sumSqrDiffError > MAX_OUTPUT_ERROR) & (runs < MAXRUNS)):
    sumSqrDiffError = 0
    for inputSetRowNr in range(ITset.shape[0]):
        IT = ITset[inputSetRowNr]
        OT = OTset[inputSetRowNr]
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

outputVectorBPN = OTset.copy()
for inputSetRowNr in range(ITset.shape[0]):
    for inputSetColNr in range(OTset.shape[1]):
        inputVectorTrainingSet = ITset[inputSetRowNr]
        outputVectorBPN[inputSetRowNr][inputSetColNr] = round(round(BPN.BPN(inputVectorTrainingSet, V0, W0)[inputSetColNr][0]),1)

print("BPN Training is ready!")
print("Runs = " + str(runs))
outputTraining = pd.DataFrame(outputVectorBPN)
outputTraining.columns = ["Output BPN"]
originalSet[outputTraining.columns] = outputTraining
print(originalSet)