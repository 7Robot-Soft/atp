#!/usr/bin/env python3

from threading import Thread
from atp import encode, decode
import argparse
import sys
import socket

class Channel:

    def __init__(self, stream, callback, proto = None, genAll = False):

        self._stream = stream

        import protos
        self._protos = protos.load(genAll)

        if proto:
            self._proto = self._protos[proto]
            for packet_name in self._proto['packets']:
                packet = self._proto['packets'][packet_name]
                if packet['direction'] == "arm":
                    pass
        else:
            self._proto = None

        def recv(id, args):
            if self._proto == None:
                if id == 255:
                    if len(args) != 1:
                        print("Warning: invalid arguments count for id %d" %id, file=sys.stderr)
                        return
                    board = args[0]
                    for proto_name in self._protos:
                        proto = self._protos[proto_name]
                        if proto["id"] == board:
                            self._proto = proto
                            print("Loading proto '%s'" %proto_name)
                            recv(id, args)
                    if self._proto == None:
                        print("Warning: unknow board %d" %board, file=sys.stderr)
                else:
                    print("Warning: no protocol loaded, can't decode id %d" %id, file=sys.stderr)
            else:
                know_packet = False
                for packet_name in self._proto['packets']:
                    packet = self._proto['packets'][packet_name]
                    if packet['id'] == id:
                        know_packet = True
                        break
                if not know_packet:
                    print("Warning: unknow packet id %d" %id, file=sys.stderr)
                    return
                if packet['direction'] != 'pic' and packet['direction'] != 'both':
                    print("Warning: ignoring arm message", file=sys.stderr)
                    return
                if len(packet['args']) != len(args) \
                        and len(packet['args']) + 2 != len(args):
                    print("Warning: expected %d arguments, %d was given"
                            %(len(packet['args']), len(args)), file=sys.stderr)
                    return
                arguments = dict(zip(packet['args'], args))
                if len(args) == len(packet['args']) + 2:
                    arguments['timestamp'] = args[-2]
                    arguments['milli'] = args[-1]
                callback(packet_name, arguments)


        thread = decode(stream, recv)

    def send(self, name, packet, *args):
        formats = list(map(lambda x: packet['args'][x], list(packet['args'])))
        encode(self._stream, packet['id'], list(zip(args, formats)))


def print_packet(name, args):
    print("[%s]" %name)
    for arg in args:
        print("\t%s:" %arg, args[arg])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Decode ATP packets with semantical traduction.')
    parser.add_argument("-p", "--proto", dest='proto')
    parser.add_argument("-c", "--connect", dest='connect', help="connect to remote host (HOST:PORT)")
    parser.add_argument("-a", "--all", dest='all', action='store_true')
    args = parser.parse_args()

    stream = sys.stdin.buffer

    if args.connect:
        try:
            host, port = args.connect.split(':')
        except ValueError:
            print("%s: error: address must be in HOST:PORT format" %sys.argv[0])
            sys.exit(1)
        try:
            port = int(port)
        except ValueError:
            print("%s: error: PORT must be an positive integer" %sys.argv[0])
            sys.exit(1)
        try:
            sock = socket.socket()
            sock.connect((host, port))
        except Exception as e:
            print("%s:" %sys.argv[0], e)
            sys.exit(1)
        file = sock.makefile(mode="rw")
        stream = file.buffer

    channel = Channel(stream, print_packet, args.proto, genAll = args.all)
