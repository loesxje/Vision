import cv2
import numpy as np
import avansvisionlibBPN as BPN
import avansvisionlib as avl
# Maximale fout die toegestaan wordt in de output voor de training input
MAX_OUTPUT_ERROR = 1E-10
# maximaal aantal runs dat uitgevoerd wordt bij het trainen
MAXRUNS = 10000

print "\n Testset laden... \n \n"

ITset, OTset = BPN.loadTrainingSet1()


print "Training input \n \n", ITset, '\n'
print "Training output \n \n", OTset, '\n'

print "BPN format: "
print "\t BPN Inputlayer  = " + str(ITset.shape[1]) + " neurons"
print "\t BPN Outputlayer = " + str(OTset.shape[1]) + " neurons"
hiddenNeurons = int(raw_input("Please choose a number of hidden neurons: "))
print "Thank You!!"

print "Initialize BPN... "

V0, W0, dV0, dW0 = BPN.initializeBPN(ITset.shape[1], hiddenNeurons, OTset.shape[1]);

print "initial values of weight matrices V0 and W0 \n*******************************************"
avl.printMatrix(V0)
avl.printMatrix(W0)

raw_input("===> PRESS ENTER")

sumSqrDiffError = MAX_OUTPUT_ERROR + 1

runs = 0

while ((sumSqrDiffError > MAX_OUTPUT_ERROR) and (runs < MAXRUNS)):
    sumSqrDiffError = 0
    for inputSetRowNr in range(ITset.shape[0]):
        IT = ITset[inputSetRowNr]
        OT = OTset[inputSetRowNr]
        OH = BPN.calculateOutputHiddenLayer(IT, V0)
        OO = BPN.calculateOutputBPN(OH, W0)
        W1, V1 = BPN.adaptVW(OT, OO, OH, IT, W0, dW0, V0, dV0)
        outputError0 = BPN.calculateOutputBPNError(OO, OT)
        outputError1 = BPN.calculateOutputBPNError(BPN(IT, V1, W1), OT)
        sumSqrDiffError += (outputError1 - outputError0) * (outputError1 - outputError0)
        V0 = V1
        W0= W1
    print "sumSqrDiffError = " + str(sumSqrDiffError)
    runs += 1
    
print "BPN Training is ready!"
print "Runs = " + str(runs)


# druk voor elke input vector uit de trainingset de output vector uit trainingset af 
# tezamen met de output vector die het getrainde BPN (zie V0, W0) genereerd bij de 
# betreffende input vector.

print "{:16} Training input {:12}| Expected Output  | Output BPN {:6}|\n"
for row in range(ITset.scale[0]):
    inputVectorTrainingSet = np.transpose(ITset[row, :])    