import trainingProgram as trainp
import testProgram as testp
import extractFeatures as ef
import time
# =================== GEEF HIER HET BIJBEHORENDE PAD OP =======================
imageWDTrain = 'C://VisionPlaatje//trainSmall//'
imageWDTest = 'C://VisionPlaatje//testSmall//'
# =============================================================================

t = time.time()
(V0,W0) = trainp.trainHandwrittenNumbers(imageWDTrain)
elapsed = time.time()-t
print("\n total time trained: {:.0f} minuten en {:.0f} seconden \n".format(elapsed/60, elapsed%60) )
results = testp.testHandwrittenNumbers(imageWDTest,V0,W0)

print("\n {:^19}|{:^8}".format("test object", "output"))
for key, value in results.items():
    for rowIterate in range(len(value)):
        if rowIterate > 0:
            key = " "
        print("{:^20}| {:^.4f}".format(key, value[rowIterate][0]))
    print(" ")

# ========================= TEST DE WEGINGSFACTOREN ===========================
# IT = np.array(ef.extractFeatures(binaryImage))
# BPN.BPN(IT,VO,WO)
# =============================================================================