import numpy as np
import cv2
import avansvisionlibSim as avl

# // TRAININGSET:  I0 because of bias V0
# //
# // setnr     I0     I1     I2    I3    I4    O1   O2
# //   1	   1.0    0.4   -0.7   0.1   0.71  0.0  0.0
# //   2       1.0    0.3   -0.5   0.05  0.34  0.0  0.0
# //   3       1.0    0.6    0.1   0.3   0.12  0.0  1.0
# //   4       1.0    0.2    0.4   0.25  0.34  0.0  1.0
# //   5	   1.0   -0.2    0.12  0.56  1.0   1.0  0.0
# //   6	   1.0	  0.1   -0.34  0.12  0.56  1.0  0.0
# //   7	   1.0   -0.6    0.12  0.56  1.0   1.0  1.0
# //   8	   1.0	  0.56  -0.2   0.12  0.56  1.0  1.0


def loadTrainingSet1():
    # input of trainingsset
    # number of columns = number of inputneurons of the BPN
    ITset = np.array([1, 0.4, -0.7, 0.1, 0.71,
                      1, 0.3, -0.5, 0.05, 0.34,
                      1, 0.6, 0.1, 0.3, 0.12,
                      1, 0.2, 0.4, 0.25, 0.34,
                      1, -0.2, 0.12, 0.56, 1.0,
                      1, 0.1, -0.34, 0.12, 0.56,
                      1, 0.6, 0.12, 0.56, 1.0,
                      1, 0.56, -0.2, 0.12, 0.56])
    ITset.resize(8, 5)

    # output of trainingset
    # number of columns = number of outputneurons of the BPN
    OTset = np.array([0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1])
    OTset.resize(8, 2)

    return [ITset, OTset]

# // TRAININGSET binary function O1 = (I1 OR I2) AND I3
# // without bias
# // setnr    I1   I2    I3   O1
# //   1	   0    0    0    0
# //   2       0    0    1    0
# //   3       0    1    0    0
# //   4       0    1    1    1
# //   5	   1    0    0    0
# //   6       1    0    1    1
# //   7       1    1    0    0
# //   8       1    1    1    1

def loadBinaryTrainingSet1():
    # input of trainingset (without bias)
    ITset = np.array([0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1,
                      1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1])
    ITset.resize(8, 3)

    # output of trainingset
    OTset = np.array([0, 0, 0, 1, 0, 1, 0, 1])
    OTset.resize(8, 1)

    return [ITset, OTset]

def loadTrainingXOR():
    # input of trainingsset
    # number of columns = number of inputneurons of the BPN
    # zonder bias

    ITset = np.array([0, 0,
                      0, 1,
                      1, 0,
                      1, 1])
    ITset.resize(4, 2)

    # output of trainingset
    # number of columns = number of outputneurons of the BPN
    OTset = np.array([0,
                      1,
                      1,
                      0])
    OTset.resize(4, 1)

    return [ITset, OTset]


def initializeBPN(inputNeurons, hiddenNeurons, outputNeurons):
    inputNeurons = int(inputNeurons)
    hiddenNeurons = int(hiddenNeurons)
    outputNeurons = int(outputNeurons)

    # Set all weightfactors to a random value
    V0 = [np.random.random() for ii in range(hiddenNeurons) for jj in range(inputNeurons)]
    V0 = np.array(V0)
    V0.resize(hiddenNeurons, inputNeurons)

    W0 = [np.random.random() for ii in range(outputNeurons) for jj in range(hiddenNeurons)]
    W0 = np.array(W0)
    W0.resize(outputNeurons, hiddenNeurons)

    # Initial modification of the weightfactors
    dV0 = [[None for row in range(inputNeurons)] for col in range(hiddenNeurons)]
    dW0 = [[None for row in range(hiddenNeurons)] for col in range(outputNeurons)]

    dV0 = avl.setValue(dV0, 0)
    dW0 = avl.setValue(dW0, 0)

    return V0, W0, dV0, dW0


# def testBPN():
#     IT = np.array([0.4, -0.7, 0.3, -0.5, 0.6, 0.1, 0.2, 0.4, 0.1, -0.2])
#     IT.resize(5, 2)
#
#     OT = np.array([0.1, 0.05, 0.3, 0.25, 0.12])
#     OT.resize((5, 1))
#
#     V0 = np.array([0.1, 0.4, -0.2, 0.2])
#     V0.resize(2, 2)
#
#     W0 = np.array([0.2, -0.5])
#     W0.resize((2, 1))
#
#     dV0 = np.array([0, 0, 0, 0])
#     dV0.resize(2, 2)
#
#     dW0 = np.array([0, 0])
#     dW0.resize(2, 1)
#
#     return [IT, OT, V0, W0, dV0, dW0]


def calculateOutputHiddenLayer(input_inputLayer, weightfactorV):
    # STEP 1: output_inputLayer = input_inputLayer
    input_inputLayer.resize(len(input_inputLayer),1)
    OI = input_inputLayer
    # STEP 2: initializing weights (already done)

    # STEP 3: calculate input_hiddenLayer
    # Vt = np.transpose(weightfactorV)
    IH = np.dot(weightfactorV, OI)

    # STEP 4: calculate output_hiddenLayer
    hiddenNeurons = weightfactorV.shape[0]
    OH = np.zeros(hiddenNeurons)
    for row in range(hiddenNeurons):
        value = 1 / (1 + np.exp(-IH[row]))
        OH[row] = value
    OH = np.array(OH)
    OH.resize(hiddenNeurons,1)
    return OH


def calculateOutputBPN(OH, W):
    # STEP 5: calculate input_outputLayer
    # Wt = np.transpose(W)
    IO = np.dot(W, OH)

    # STEP 6: calculate output_outputLayer
    outputNeurons = W.shape[0]
    OO = []
    for row in range(outputNeurons):
        value = 1 / (1 + np.exp(- IO[row]))
        OO.append(value)
    OO = np.array(OO)
    OO.resize(outputNeurons, 1)

    return OO


def calculateOutputBPNError(OO, OT):
    # STEP 7: calculate the error
    sumSqrErr = 0
    diff = 0
    for row in range(OT.shape[0]):
        diff = OT[row] - OO[row]
        sumSqrErr += (diff * diff)
    outputError = 0.5 * sumSqrErr

    return outputError

# def getMultiplication(firstMatrix,  matrixToMultipyWith, outputShape):
#     rowsFM = firstMatrix.shape[0]
#     rowsMTMW = outputShape.shape[0]
#     newMatrix = [[0 for row in range(rowsFM)] for col in range(rowsMTMW)]
#     for col in range(rowsMTMW):
#         for row in range(rowsFM):
#             entrydStarT = np.dot(firstMatrix[row], matrixToMultipyWith[0][col])
#             newMatrix[[col][0]][row] = entrydStarT
#     newMatrix = np.array(newMatrix)
#     newMatrix.resize(rowsMTMW,rowsFM)



def adaptVW(OT, OO, OH, OI, W0, dW0, V0, dV0):
    # adapt weightfactors W
    # STEP 8:
    ALPHA = 1
    ETHA = 0.6
    nrOutPutTrSet = OT.shape[0]
    OT = np.array(OT)
    OT.resize(nrOutPutTrSet,1)
    OOerror = OT - OO

    d = []
    for row in range(nrOutPutTrSet):
        di = (OT[row, 0] - OO[row, 0]) * OO[row, 0] * (1 - OO[row, 0])
        d.append(di)
    d = np.array(d)
    #d.resize(nrOutPutTrSet, 1)

    Y = [[0 for r in range(OH.shape[0])] for c in range(nrOutPutTrSet)]
    for j in range(nrOutPutTrSet):
        for i in range(OH.shape[0]):
            entry = np.dot(OH[i],d[j])
            Y[[j][0]][i] = entry
    Y = np.array(Y)
    Y.resize(nrOutPutTrSet, OH.shape[0])


    # STEP 9:
    dW = ALPHA * dW0 + ETHA * Y

    # adapt weightfactors V
    # STEP 10:
    OHerror = np.dot(W0.transpose(),d)
    OHerror.resize(OH.shape[0], 1)

    # STEP 11:
    dStar = [0 for r in range(OH.shape[0])]
    for row in range(OH.shape[0]):
        dStari = OHerror[row, 0] * OH[row, 0] * (1 - OH[row, 0])
        dStar[row] = dStari
    dStar = np.array(dStar)
    dStar.resize(OH.shape[0], 1)

    # STEP 12:
    dStarT = np.transpose(dStar)
    X = [[0 for r in range(OI.shape[0])] for c in range(OH.shape[0])]
    for col in range(OH.shape[0]):
        for row in range(OI.shape[0]):
            entrydStarT = np.dot(OI[row], dStarT[0][col])
            X[[col][0]][row] = entrydStarT
    # X = OI * dStarT
    X = np.array(X)
    X.resize(OH.shape[0], OI.shape[0])

    # STEP 13
    dV = ALPHA * dV0 + ETHA * X

    # Update matrices with weightfactors
    # STEP 14:
    V = V0 + dV
    W = W0 + dW

    return V, W


def BPN(II, V, W):
    OH = calculateOutputHiddenLayer(II, V)
    OO = calculateOutputBPN(OH, W)
    return OO