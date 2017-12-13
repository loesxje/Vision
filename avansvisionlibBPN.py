import numpy as np
import cv2
import avansvisionlib as avl

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
    ITset.resize(8,5)

    # output of trainingset
    # number of columns = number of outputneurons of the BPN
    OTset = np.array([0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1])
    OTset.resize(8,2)

    return [ITset, OTset]
# =============================================================================
# def loadBinaryTrainingSet1():
#     # input of trainingset (without bias)
#     ITset = np.array([0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1,
#                       1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1])
#     ITset.resize(8,3)
# 
#     # output of trainingset
#     OTset = np.array([0, 0, 0, 1, 0, 1, 0, 1])
#     OTset.resize(8,1)
# 
#     return [ITset, OTset]
# =============================================================================

def initializeBPN(inputNeurons, hiddenNeurons, outputNeurons):
    inputNeurons = int(inputNeurons)
    hiddenNeurons = int(hiddenNeurons)
    outputNeurons = int(outputNeurons)

    # Set all weightfactors to a random value
    V0 = [np.random.random() for ii in range(inputNeurons) for jj in range(hiddenNeurons)]
    V0 = np.array(V0)
    V0.resize(inputNeurons, hiddenNeurons)

    W0 = [np.random.random() for ii in range(hiddenNeurons) for jj in range(outputNeurons)]
    W0 = np.array(W0)
    W0.resize(hiddenNeurons, outputNeurons)
    avl.printMatrix(W0)
    # Initial modification of the weightfactors
    dV0 = [[ None for row in range(inputNeurons)] for col in range(hiddenNeurons)]
    dW0 = [[ None for row in range(hiddenNeurons)] for col in range(outputNeurons)]

    dV0 = avl.setValue(dV0, 0)
    dW0 = avl.setValue(dW0, 0)

    return [V0, W0, dV0, dW0]

# =============================================================================
# def testBPN():
#     IT = np.array([0.4, -0.7, 0.3, -0.5, 0.6, 0.1, 0.2, 0.4, 0.1, -0.2])
#     IT.resize(5,2)
# 
#     OT = np.array([0.1, 0.05, 0.3, 0.25, 0.12])
#     OT.resize((5,1))
# 
#     V0 = np.array([0.1, 0.4, -0.2, 0.2])
#     V0.resize(2,2)
# 
#     W0 = np.array([0.2, -0.5])
#     W0.resize((2,1))
# 
#     dV0 = np.array([0, 0, 0, 0])
#     dV0.resize(2,2)
# 
#     dW0 = np.array([0, 0])
#     dW0.resize(2,1)
# 
#     return [IT, OT, V0, W0, dV0, dW0]
# =============================================================================

def calculateOutputHiddenLayer(input_inputLayer, weightfactorV):
    # STEP 1: output_inputLayer = input_inputLayer
    OI = input_inputLayer.copy()

    # STEP 2: initializing weights (already done)

    # STEP 3: calculate input_hiddenLayer
<<<<<<< HEAD
    #Vt = np.transpose(weightfactorV)
    IH = np.dot(weightfactorV, OI)
    print IH
    # STEP 4: calculate output_hiddenLayer
    hiddenNeurons = weightfactorV.shape[0]
    # OH = np.array([])
    # OH.resize(hiddenNeurons, 1)
    OH = np.zeros(hiddenNeurons)
=======
#    Vt = np.transpose(weightfactorV)
    IH = np.dot(weightfactorV, OI)

    # STEP 4: calculate output_hiddenLayer
    hiddenNeurons = weightfactorV.shape[1]
    OH = np.zeros([hiddenNeurons, 1])
>>>>>>> 8a71149c2e4f2e92c0561f0b28feb01839cf4b57
    for row in range(hiddenNeurons):
        value = 1 / (1 + np.exp(-IH[row]))
        OH[row] = value

    return OH

def calculateOutputBPN(OH, W):
    # STEP 5: calculate input_outputLayer
<<<<<<< HEAD
    #Wt = np.transpose(W)
=======
#    Wt = np.transpose(W)
>>>>>>> 8a71149c2e4f2e92c0561f0b28feb01839cf4b57
    IO = np.dot(W, OH)

    # STEP 6: calculate output_outputLayer
    outputNeurons = W.shape[1]
    OO =  np.zeros([outputNeurons, 1])
    for row in range(outputNeurons):
<<<<<<< HEAD
        value = 1 / (1 + np.exp(- IO[row]))
        OO.append(value)
    OO = np.array(OO)
    OO.resize(outputNeurons, 1)
=======
        value = 1 / (1 + np.exp(- IO[row, 0]))
        OO[row, 0] = value

>>>>>>> 8a71149c2e4f2e92c0561f0b28feb01839cf4b57

    return OO

def calculateOutputBPNError(OO, OT):
    # STEP 7: calculate the error
    sumSqrErr = 0
    diff = 0
    for row in range(OT.shape[0]):
        een =  OT[row, 0]
        twee = OO[row, 0]
        diff = 1
        # diff = OT[row, 0] - OO[row, 0]
        sumSqrErr += (diff * diff)
    outputError = 0.5 * sumSqrErr

    return outputError


def adaptVW(OT, OO, OH, OI, W0, dW0, V0, dV0, ALPHA = 1, ETA = 0.6):
    # adapt weightfactors W
    # STEP 8:
    OOerror = OT - OO

    d = []
    for row in range(OT.shape[0]):
        di = (OT[row, 0] - OO[row, 0]) * OO[row, 0] * (1 - OO[row, 0])
        d.append(di)
    d.resize(OT.shape[0], 1)

    dt = np.transpose(d)
<<<<<<< HEAD
    Y = np.dot(OH, dt)
=======
    Y = np.multiply(OH, dt)
>>>>>>> 8a71149c2e4f2e92c0561f0b28feb01839cf4b57
    Y.resize(OH.shape[0], OT.shape[0])

    # STEP 9:
    dW = ALPHA * dW0 + ETA * Y
    dW.resize(OH.shape[0], OT.shape[0])

    # adapt weightfactors V
    # STEP 10:
    OHerror = W0 * d
    OH.resize(OH.shape[0], 1)
    
    dStar = np.zeros([OH.shape[0], 1])
    # STEP 11:
    for row in range(OH.shape[0]):
        dStari = OHerror[row, 0] * OH[row, 0] * (1 - OH[row, 0])
        dStar[row, 0] = dStari

    # STEP 12:
    dStarT = np.transpose(dStar)
    X = OI * dStarT
    X.resize(OI.shape[0], OH.shape[0])

    # STEP 13
    dV = ALPHA * dV0 + ETA * X

    # Update matrices with weightfactors
    # STEP 14:
    V = V0 + dV
    V.resize(V0.shape[0], V0.shape[1])
    W = W0 + dW
    W.resize(W0.shape[0], W0.shape[1])
    

def BPN(II, V, W):
    OH = calculateOutputHiddenLayer(II, V)
    OO = calculateOutputBPN(OH, W)
    return OO