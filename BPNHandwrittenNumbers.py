import trainingProgram as trainp
import testProgram as testp
import extractFeatures as ef

# =================== GEEF HIER HET BIJBEHORENDE PAD OP =======================
imageWDTrain = 'C://VisionPlaatje//trainSmall//'
imageWDTest = 'C://VisionPlaatje//testSmall//'
# =============================================================================

(V0,W0) = trainp.trainHandwrittenNumbers(imageWDTrain)
testp.testHandwrittenNumbers(imageWDTest,V0,W0)

# ========================= TEST DE WEGINGSFACTOREN ===========================
# IT = np.array(ef.extractFeatures(binaryImage))
# BPN.BPN(IT,VO,WO)
# =============================================================================