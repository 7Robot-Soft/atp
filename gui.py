#!/usr/bin/env python3

import sys, os
from PyQt4 import QtCore, QtGui
import protos
from protos import Proto
from packet import Packet
import inspect
from channel import Channel

import socket

class AtpSender(QtGui.QTabWidget):

    def __init__(self):
        super(AtpSender, self).__init__()
        self.initUI()
        self.error = QtGui.QErrorMessage()

    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.resize(300, 500)
        self.setWindowTitle('ATP Sender')

        for name, obj in inspect.getmembers(protos,
                lambda x: inspect.isclass(x) and issubclass(x, Proto)):
            if name != "Proto":
                self.addTab(self.createProto(name, obj), name)

        self.show()

    def createProto(self, name, proto):
        scroll = QtGui.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameStyle(QtGui.QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        layout = QtGui.QVBoxLayout()
        widget = QtGui.QWidget()
        sock = socket.socket()
        sock.connect(("localhost", 1300 + proto.type))
        chan = Channel(proto, sock, lambda: None, genAll = True)
        for attrn in sorted(proto.__dict__):
            attr = proto.__getattribute__(proto, attrn)
            if isinstance(attr, Packet):
                packet = self.createPacket(attrn, attr, chan)
                layout.addWidget(packet, 0)
        widget.setLayout(layout)
        scroll.setWidget(widget)
        return scroll

    def createPacket(self, name, packet, chan):
        group = QtGui.QGroupBox(name)
        group.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        layout = QtGui.QGridLayout()
        texts = []
        row = 0
        eventHandler = lambda: self.send(packet, texts, chan)
        for arg, type in packet.attrs:
            label = QtGui.QLabel(arg)
            text = QtGui.QLineEdit()
            texts.append([arg, text])
            text.returnPressed.connect(eventHandler)
            layout.addWidget(label, row, 0)
            layout.addWidget(text, row, 1)
            row = row + 1
        send = QtGui.QPushButton("Send")
        send.clicked.connect(eventHandler)
        layout.addWidget(send, row, 0, row, 2)
        group.setLayout(layout)
        return group

    def send(self, packet, texts, chan):
        args = list(map(lambda x: x[1].text(), texts))
        try:
            chan._send(None, packet, *args)
        except Exception as e:
            self.error.showMessage(str(e))

def main():

    app = QtGui.QApplication(sys.argv)

    sender = AtpSender()

    os._exit(app.exec_())


if __name__ == '__main__':
    main()
