import sACNTools
import screenCapture
import rasterViewer
import ACNCaptureWorker
import ACNStreamWorker
import ScreenCaptureWorker
import sys

from PyQt4 import QtCore, QtGui
x = 32
y =32

class Main(QtGui.QMainWindow):
    capData = []
    def __init__(self):
        super(Main, self).__init__()
        print "Initializing sACN"
        sACNTools.init("127.0.0.1")

        print "Creating raster viewer on main thread..."
        self.imageLabel = rasterViewer.rasterViewer(x,y)
        self.imageLabel.show()
        self.imageLabel.setCallback(self.getData)
        self.setCentralWidget(self.imageLabel)

        print "Starting screen capture worker thread..."
        self.scrnCapThread = ScreenCaptureWorker.ScreenCaptureWorker(x,y)
        self.scrnCapThread.setMainThread(self)
        self.scrnCapThread.start()

        print "Starting sACN stream worker thread..."
        self.sACNStream = ACNStreamWorker.ACNStreamWorker()
        self.sACNStream.setMainThread(self)
        self.sACNStream.start()

    def getData(self):
        return self.capData

    def setData(self, data):
        self.capData = data

if __name__ == '__main__':
    print "starting..."
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
