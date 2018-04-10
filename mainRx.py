# import sACNTools
# import sys
# sACNTools.init("239.255.0.1")
# print "Running sACN Capture"
# while(1):
#     ACN = sACNTools.capturesACN()
#     sys.stdout.write("%s\r" % str(ACN["DMP"]["propertyValues"][0:10]))
#     sys.stdout.flush()
#
import sACNTools

import rasterViewer
import ACNCaptureWorker
import numpy as np
import ACNStreamWorker

import sys

from PyQt4 import QtCore, QtGui
x = 32
y =32

class MainRx(QtGui.QMainWindow):
    numUniverses = np.ceil(x*y/512).astype(int)
    capData = [0]*numUniverses
    def __init__(self):
        super(MainRx, self).__init__()
        print "Initializing sACN"
        sACNTools.init("127.0.0.1")




        print "initializing acn capture..."
        self.captureWorker = ACNCaptureWorker.ACNCaptureWorker()
        self.captureWorker.setMainThread(self)
        self.captureWorker.start()

        print "Creating raster viewer on main thread..."
        self.imageLabel = rasterViewer.rasterViewer(x, y)
        self.imageLabel.show()
        self.imageLabel.setCallback(self.getData)
        self.setCentralWidget(self.imageLabel)

    def getData(self):
        #self.imageLabel.open();
        return self.capData

    def setData(self, data):
       # print "new data"
        start = (data[0]*512)
        self.capData[start:start+512] = data[1]


if __name__ == '__main__':
    print "starting..."
    app = QtGui.QApplication(sys.argv)
    main = MainRx()
    main.show()
    sys.exit(app.exec_())
