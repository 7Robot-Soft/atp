#!/usr/bin/env python3

import sys, os
from PyQt4 import QtCore, QtGui
from channel import Channel
import protos
import socket


class AtpSender(QtGui.QTabWidget):

    def __init__(self):
        super(AtpSender, self).__init__()
        self.protos = protos.load()
        self.error = QtGui.QErrorMessage()
        self.initUI()

    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.resize(300, 500)
        self.setWindowTitle('ATP Sender')

        for proto in self.protos:
            self.addTab(self.createProto(proto, self.protos[proto]), proto)

        self.show()

    def createProto(self, name, proto):
        scroll = QtGui.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameStyle(QtGui.QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        layout = QtGui.QVBoxLayout()
        widget = QtGui.QWidget()
        sock = socket.socket()
        sock.connect(("localhost", 1300 + proto["id"]))
        file = sock.makefile(mode="rw")
        chan = Channel(file.buffer, lambda: None, proto = name, genAll = True)
        chan._file_ = file # archi moche
        for packet in proto['packets']:
            layout.addWidget(self.createPacket(packet, proto['packets'][packet], chan), 0)
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
        for arg in packet['args']:
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
            chan.send(None, packet, *args)
        except Exception as e:
            self.error.showMessage(str(e))

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)

    sender = AtpSender()

    os._exit(app.exec_())
