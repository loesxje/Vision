from skimage import measure
import numpy as np
import cv2
import avansvisionlibSim as avl
import boundingBoxesSim as bobo
import mnist
import pandas as pd

trainData = mnist.read(dataset='data0', path='C:/VisionPlaatje/Mnist')

#for ii in range(len(trainData)):
    