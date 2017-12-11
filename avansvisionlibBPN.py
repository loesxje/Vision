import numpy as np
import cv2
import avansvisionlib as avl

def loadTrainingSet1():
    global ITset, OTset
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
    global ITset, OTset
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
    V0 = [np.random.random() for i in range(inputNeurons) for j in range(hiddenNeurons)]
    V0 = np.array(V0)
    V0.resize(inputNeurons, hiddenNeurons)

    W0 = [np.random.random() for i in range(hiddenNeurons) for j in range(outputNeurons)]
    W0 = np.array(W0)
    W0.resize(hiddenNeurons, outputNeurons)

    # Initial modification of the weightfactors

    return V0

