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

def loadBinaryTrainingSet1():
    # input of trainingset (without bias)
    ITset = np.array([0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1,
                      1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1])
    ITset.resize(8,3)

    # output of trainingset
    OTset = np.array([0, 0, 0, 1, 0, 1, 0, 1])
    OTset.resize(8,1)

    return [ITset, OTset]

def initializeBPN(inputNeurons, hiddenNeurons, outputNeurons):
    # Set all weightfactors to a random value
    V0 = [np.random.random() for ii in range(inputNeurons) for jj in range(hiddenNeurons)]
    V0 = np.array(V0)
    V0.resize(inputNeurons, hiddenNeurons)

    W0 = [np.random.random() for ii in range(hiddenNeurons) for jj in range(outputNeurons)]
    W0 = np.array(W0)
    W0.resize(hiddenNeurons, outputNeurons)

    # Initial modification of the weightfactors
    dV0 = [[ None for row in range(inputNeurons)] for col in range(hiddenNeurons)]
    dW0 = [[ None for row in range(hiddenNeurons)] for col in range(outputNeurons)]

    dV0 = avl.setValue(dV0, 0)
    dW0 = avl.setValue(dW0, 0)

    return [V0, W0, dV0, dW0]

def testBPN():
    IT = np.array([0.4, -0.7, 0.3, -0.5, 0.6, 0.1, 0.2, 0.4, 0.1, -0.2])
    IT.resize(5,2)

    OT = np.array([0.1, 0.05, 0.3, 0.25, 0.12])
    OT.resize((5,1))

    V0 = np.array([0.1, 0.4, -0.2, 0.2])
    V0.resize(2,2)

    W0 = np.array([0.2, -0.5])
    W0.resize((2,1))

    dV0 = np.array([0, 0, 0, 0])
    dV0.resize(2,2)

    dW0 = np.array([0, 0])
    dW0.resize(2,1)

    return [IT, OT, V0, W0, dV0, dW0]

def calculateOutputHiddenLayer(input_inputLayer, weightfactorV):
    # STEP 1: output_inputLayer = input_inputLayer
    OI = input_inputLayer.copy()

    # STEP 2: initializing weights (already done)

    # STEP 3: calculate input_hiddenLayer
    Vt = np.transpose(weightfactorV)
    IH = np.multiply(Vt, OI)

    # STEP 4: calculate output_hiddenLayer
    hiddenNeurons = weightfactorV.shape[1]
    OH = np.array([])
    OH.resize(hiddenNeurons, 1)
    for row in range(hiddenNeurons):
        value = 1 / (1 + np.exp(-IH[row, 0]))
        OH[row, 0] = value

    return OH

def calculateOutputBPN(OH, W):
    # STEP 5: calculate input_outputLayer
    Wt = np.transpose(W)
    IO = np.multiply(Wt, OH)

    # STEP 6: calculate output_outputLayer
    outputNeurons = W.shape[1]
    OO = np.array([])
    OO.resize(outputNeurons, 1)
    for row in range(outputNeurons):
        value = 1 / (1 + np.exp(- IO[row, 0]))
        OO[row, 0] = value

    return OO

def calculateOutputBPNError(OO, OT):
    # STEP 7: calculate the error
    sumSqrErr, diff = 0
    for row in range(OT.shape[0]):
        


