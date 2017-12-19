import trainingProgram as trainp
import testProgram as testp
import extractFeatures as ef

# =================== GEEF HIER HET BIJBEHORENDE PAD OP =======================
imageWDTrain = '/Users/Eva/Workspace_programs/PycharmProjects/Vision-master/Pictures/train//'
imageWDTest = '/Users/Eva/Workspace_programs/PycharmProjects/Vision-master/Pictures/test//'
# =============================================================================

(V0,W0) = trainp.trainHandwrittenNumbers(imageWDTrain)
testp.testHandwrittenNumbers(imageWDTest,V0,W0)

# ========================= TEST DE WEGINGSFACTOREN ===========================
# IT = np.array(ef.extractFeatures(binaryImage))
# BPN.BPN(IT,VO,WO)
# =============================================================================