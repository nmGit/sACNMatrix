from PyQt4 import QtCore, QtGui
import sACNTools

class ACNCaptureWorker(QtCore.QThread):
    mainThread = 0
    capData = []
    x = 0
    y = 0

    def __init__(self):
        print "initializing parent of capture worker..."
        super(ACNCaptureWorker, self).__init__()
        print "done."

    def run(self):
        while(1):
            #print "capturing..."
            data = sACNTools.capturesACN()
            data = (data["Framing"]["universe"],data["DMP"]["propertyValues"])
            #print data[0]
            self.mainThread.setData(data)

    def setMainThread(self,m):
        self.mainThread = m



