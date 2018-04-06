from PyQt4 import QtCore, QtGui

class ACNCaptureWorker(QtCore.QThread):
    mainThread = 0
    capData = []
    x = 0
    y = 0

    def __init__(self):
        super(ACNCaptureWorker, self).__init__()

    def run(self):
        while(True):
            print "Hi"
            self.sleep(2)

    def setMainThread(self,m):
        self.mainThread = m



