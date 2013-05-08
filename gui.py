#!/usr/bin/env python3

import sys, os
from PyQt4 import QtCore, QtGui
from channel import Channel, print_packet
import protos
import socket
import argparse
from settings import PORT, HOST


class AtpSender(QtGui.QTabWidget):

    def __init__(self, **kwargs):
        super(AtpSender, self).__init__()
        self.port = PORT
        self.host = HOST
        self.symmetrical = False
        for arg in kwargs:
            if arg == 'host':
                self.host = kwargs[arg]
            elif arg == 'port':
                self.port = int(kwargs[arg])
            elif arg == 'symmetrical':
                self.symmetrical = kwargs[arg]
            else:
                print("Warning: unexpected '%s' argument" %arg, file=sys.stderr)
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
        try:
            sock.connect((self.host, self.port + proto["id"]))
        except:
            print ("Failed to connect on %s %d" % (self.host, self.port))
            sys.exit(-1)
        file = sock.makefile(mode="rw")
        chan = Channel(file.buffer, print_packet, proto = name,
                symmetrical = self.symmetrical)
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
        eventHandler = lambda: self.send(name, packet, texts, chan)
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

    def send(self, name, packet, texts, chan):
        args = list(map(lambda x: x[1].text(), texts))
        try:
            chan.send(name, packet, *args)
        except Exception as e:
            self.error.showMessage(str(e))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='GUI to send ATP packets.', add_help=False)
    parser.add_argument('-h', '--host', dest='host', default=HOST, help='connect to remote host')
    parser.add_argument('-p', '--port', dest='port', default=PORT, help='port offset')
    parser.add_argument('-s', '--symmetrical', action='store_true', dest='symmetrical', help='symmetrical packets')
    args = parser.parse_args()

    app = QtGui.QApplication(sys.argv)

    sender = AtpSender(host = args.host, port = args.port,
            symmetrical = args.symmetrical)

    os._exit(app.exec_())
