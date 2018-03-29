from PyQt4 import QtCore, QtGui
import numpy as np


class rasterViewer(QtGui.QWidget):
    datasource = 0
    szx = 1
    szy = 1
    def __init__(self, szx, szy):
        super(rasterViewer, self).__init__()

        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setScaledContents(True)
        self.layout = QtGui.QHBoxLayout()
        self.setWindowTitle("Image Viewer")
        self.resize(640, 480)
        self.imageLabel.show()
        self.layout.addWidget(self.imageLabel)
        self.setLayout(self.layout)
        self.szx = szx
        self.szy = szy
        self.start()

    def start(self):
        print "starting timer"
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.open)
        timer.start(60) #30 Hz
        print "starting raster viewer"

    def setCallback(self, cb):
        self.datasource = cb

    def open(self):
        pilimg = np.array(self.datasource())
        image = QtGui.QImage(pilimg, self.szx, self.szy, QtGui.QImage.Format_RGB32)
        image.setColorCount(3)
        if image.isNull():
            QtGui.QMessageBox.information(self, "Image Viewer","Cannot load %s." % fileName)
            return

        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image).scaledToHeight(200, QtCore.Qt.FastTransformation))
       # self.imageLabel.adjustSize()


