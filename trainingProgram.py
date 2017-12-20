import cv2
import numpy as np
import avlBPNEvaWorking as BPN
import avansvisionlib as avl
import pandas as pd
import os
import extractFeatures as ef

def trainHandwrittenNumbers(imageWD):

    # Maximale fout die toegestaan wordt in de output voor de training input
    MAX_OUTPUT_ERROR = 1E-8
    # maximaal aantal runs dat uitgevoerd wordt bij het trainen
    MAXRUNS = 10000

    imageCodes = []

    for file in os.listdir(imageWD):  # +folder
        if file != ".DS_Store":
            numberOfInputs = len(os.listdir(imageWD))
            imageCodes.append(file)
        image = ef.makeBinaryImage(imageWD + file)

    # print(imageCodes)
    # avl.show16SImageStretch(image, "image")

    numberOfFeatures = image.size + 1
    numberOfOutputs = 4

    print("\n Testset laden... \n \n")
    print("\t BPN Inputlayer  = " + str(numberOfInputs) + " neurons")
    print("\t BPN Outputlayer = " + str(numberOfOutputs) + " neurons")
    hiddenNeurons = int(input("Please choose a number of hidden neurons: "))
    print("Thank You!!")

    print("Initialize BPN... ")

    V0, W0, dV0, dW0 = BPN.initializeBPN(numberOfFeatures, hiddenNeurons, numberOfOutputs)

    #perimeterMax, areaMax = ef.memoriseLargest(imageWD)
    counter = 0
    totalImg = len(imageCodes)
    # Haal de afbeeldingen uit de map.
    for i in range(totalImg):
        # TODO: random aanpassen
        counter += 1
        print("image {} out of {}".format(counter, totalImg))
        indexnummer = np.random.randint(len(imageCodes))
        filename = imageCodes.pop(indexnummer)
        print("load image {}".format(filename))
        binaryImage = ef.makeBinaryImage(imageWD + filename)

        runs = 0

        sumSqrDiffError = MAX_OUTPUT_ERROR + 1
        # looping over afbeeldingen met eenen,tweeen drieen, vieren, vijfen, zessen enz
        # Voor elke feature worden de weights bepaald
        
        # bepaal de input en output van de traindata
        IT = np.array(ef.extractFeatures(binaryImage))
        OT = np.array(ef.outputHandwrittenNumbers(filename))
        ITold = np.zeros(IT.shape)
        print(np.sum(ITold-IT))
        
        ITold = IT
        
        
        while ((sumSqrDiffError > MAX_OUTPUT_ERROR) & (runs < MAXRUNS)):
            sumSqrDiffError = 0
            #     for inputSetRowNr in range(ITset.shape[0]):  # Afbeeldingen in de map
            # for inputSetRowNr in range(binaryImage.shape[0]):

            OH = BPN.calculateOutputHiddenLayer(IT, V0)
            OO = BPN.calculateOutputBPN(OH, W0)
            [V1, W1, dV1, dW1] = BPN.adaptVW(OT, OO, OH, IT, W0, dW0, V0, dV0)
            
            #calculate model error
            outputError0 = BPN.calculateOutputBPNError(OO, OT)
            outputError1 = BPN.calculateOutputBPNError(BPN.BPN(IT, V1, W1), OT)
            sumSqrDiffError += (outputError1 - outputError0) * (outputError1 - outputError0)
            
            #save weights
            V0 = V1
            W0 = W1
            dV0 = dV1
            dW0 = dW1
            
            #print("sumSqrDiffError = " + str(sumSqrDiffError))
            runs += 1
        print("Runs = " + str(runs))
        print()
    # Print de output
    # outputVectorBPN = OTset.copy()
    # for inputSetRowNr in range(ITset.shape[0]):
    #     for inputSetColNr in range(OTset.shape[1]):
    #         inputVectorTrainingSet = ITset[inputSetRowNr]
    #         outputVectorBPN[inputSetRowNr][inputSetColNr] = round(round(BPN.BPN(inputVectorTrainingSet, V0, W0)[inputSetColNr][0]), 1)
    #
    print("BPN Training is ready!")
    print(V0)
    print(W0)
    return V0, W0

    # outputTraining = pd.DataFrame(outputVectorBPN)
    # outputTraining.columns = ["Output BPN"]
    # originalSet[outputTraining.columns] = outputTraining
    # print(originalSet)