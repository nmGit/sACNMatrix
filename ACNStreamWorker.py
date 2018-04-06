import sACNTools
from PyQt4 import QtCore, QtGui

class ACNStreamWorker(QtCore.QThread):
    numUniverses = 0
    universeSize = 512
    mainThread = 0
    data = 0
    def __init__(self):
        super(ACNStreamWorker, self).__init__()


    def setMainThread(self,m):
        self.mainThread = m

    def setData(self, data):
        self.data = data
        self.numUniverses = len(self.data) % self.universeSize


    def run(self):
        while(1):

            self.data = self.mainThread.getData()
            print self.data
            self.numUniverses = len(self.data) / self.universeSize
            print "number of universes:",self.numUniverses
            for i in range(self.numUniverses):
                unidata = []
                for y in range(self.universeSize):
                    unidata.append(self.data[i*self.universeSize+y])
                print "sending universe:",i, unidata
                sACNTools.sendsACN(i,0,unidata)


