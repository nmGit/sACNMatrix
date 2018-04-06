from PyQt4 import QtCore, QtGui
import screenCapture
class ScreenCaptureWorker(QtCore.QThread):
    capData = []
    mainThread = 0
    def __init__(self, x, y):
        super(ScreenCaptureWorker, self).__init__()
        self.x = x
        self.y = y

    def run(self):
        while(1):
            if (self.x is 0 or self.y is 0):
                print "ERROR: You must set capture dimensions"
            self.capData = screenCapture.getScreenPixels(self.x, self.y)
            self.mainThread.setData(self.capData)
            #threading.Timer(0.033, self.screenCap).start()

    def setMainThread(self,m):
        self.mainThread = m

    def getData(self):
        return self.capData

    def setData(self, data):
        self.capData = data
