import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import data, exposure

def retrieveHOG(inputMatrix, doPlot = False):
    image = inputMatrix.copy()
    fd, hogImage = hog(image, orientations=8, pixels_per_cell=(16, 16),
                    cells_per_block=(1, 1), visualise=True)
    
    hogVector = np.zeros((hogImage.size, 1))
    nRows = hogImage.shape[0]
    nCols = hogImage.shape[1]
    
    
    index = 0
    for cols in range(nCols):
        for rows in range(nRows):
            hogVector[index] = hogImage[rows][cols]
            index += 1
    
    if doPlot: 
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)
    
        ax1.axis('off')
        ax1.imshow(image, cmap=plt.cm.gray)
        ax1.set_title('Input image')
        ax1.set_adjustable('box-forced')
        
        # Rescale histogram for better display
        hogImage_rescaled = exposure.rescale_intensity(hogImage, in_range=(0, 10))
        
        ax2.axis('off')
        ax2.imshow(hogImage_rescaled, cmap=plt.cm.gray)
        ax2.set_title('Histogram of Oriented Gradients')
        ax1.set_adjustable('box-forced')
        plt.show()
    return [hogImage, hogVector]