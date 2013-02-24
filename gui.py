#!/usr/bin/env python3

import sys
from PyQt4 import QtCore, QtGui
import protos
from protos import Proto
from packet import Packet
import inspect

class AtpSender(QtGui.QTabWidget):

    def __init__(self):
        super(AtpSender, self).__init__()
        self.initUI()

    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        #self.resize(250, 150)
        self.setWindowTitle('ATP Sender')

        for name, obj in inspect.getmembers(protos,
                lambda x: inspect.isclass(x) and issubclass(x, Proto)):
            if name != "Proto":
                self.addTab(self.createProto(name, obj), name)

        self.show()

    def createProto(self, name, proto):
        tab = QtGui.QTabWidget()
        for attrn in sorted(proto.__dict__):
            attr = proto.__getattribute__(proto, attrn)
            if isinstance(attr, Packet):
                tab.addTab(self.createPacket(attrn, attr), attrn)
        return tab

    def createPacket(self, name, packet):
        tab = QtGui.QTabWidget()
        return tab

def main():

    app = QtGui.QApplication(sys.argv)

    sender = AtpSender()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
