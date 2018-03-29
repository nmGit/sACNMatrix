import sACNCapture
import screenCapture
import rasterViewer
import numpy as np
import threading
import time
import sys
from PyQt4 import QtCore, QtGui
x = 32
y =32

class ACNStreamer(QtGui.QMainWindow):
    capData = []
    def __init__(self):
        super(ACNStreamer, self).__init__()
        self.scrnCapThread = ACNCaptureWorker()

        print "starting thread"
        self.scrnCapThread.setMainThread(self)
        self.scrnCapThread.start()
        self.scrnCapThread.screenCap()

        print "creating raster viewer"
        self.imageLabel = rasterViewer.rasterViewer(x,y)
        self.imageLabel.show()
        self.imageLabel.setCallback(self.getData)
        self.setCentralWidget(self.imageLabel)

    def getData(self):
        return self.capData
    def setData(self, data):
        self.capData = data

class ACNCaptureWorker(QtCore.QThread):
    mainThread = 0
    capData = []
    def run(self):
        while(True):
            print "Hi"
            self.sleep(2)
    def setMainThread(self,m):
        self.mainThread = m
    def screenCap(self):

        #print "Getting caputre"
        self.capData =  screenCapture.getScreenPixels(x,y)
        self.mainThread.setData(self.capData)
        threading.Timer(0.033, self.screenCap).start()

        # ras = rasterViewer.rasterViewer(x,y)
        # ras.setCallback(getscrnpixelscb)
        #
        # ras.show()
        # ras.start()

if __name__ == '__main__':
    print "starting..."
    app = QtGui.QApplication(sys.argv)
    main = ACNStreamer()
    main.show()
    sys.exit(app.exec_())
