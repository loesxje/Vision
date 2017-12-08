from skimage import measure
import numpy as np
import cv2
import avansvisionlibSim as avl
import sys
import boundingBoxesSim as bobo
import mnist
import pandas as pd

trainData = list(mnist.read(dataset='training', path='.\mnist'))

mnist.show(trainData[0][1])