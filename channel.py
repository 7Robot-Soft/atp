#!/usr/bin/env python3

from threading import Thread
from atp import encode, decode
import argparse
import sys
import socket
from logging import getLogger
from symmetrical import symmetrical

class Channel:

    def __init__(self, stream, callback, **kwargs):

        self._logger = getLogger("comm.channel")

        transmitter = "arm"
        follow = False
        proto = None
        self._symmetrical = False

        for arg in kwargs:
            if arg == "transmitter":
                if kwargs[arg] != None:
                    transmitter = kwargs[arg]
            elif arg == "follow":
                if kwargs[arg] != None:
                    follow = kwargs[arg]
            elif arg == "proto":
                if kwargs[arg] != None:
                    proto = kwargs[arg].capitalize()
            elif arg == "symmetrical":
                if kwargs[arg] != None:
                    self._symmetrical = kwargs[arg]
            else:
                self._logger.warning("unexpected '%s' argument" %arg)

        self._stream = stream

        import protos
        self._protos = protos.load()
        self._proto = None
        self._proto_name = None

        if proto:
            try:
                self._proto = self._protos[proto]
            except KeyError:
                pass

            if not self._proto:
                raise Exception("Unknow protocol '%s', " \
                        "available protocols: %s" \
                        %(proto, ','.join(self._protos.keys())))

            for packet_name in self._proto['packets']:
                packet = self._proto['packets'][packet_name]
                if packet['transmitter'] == transmitter or packet['transmitter'] == 'both' or transmitter == 'both':
                    self.__setattr__(packet_name, self._create_method(packet_name, packet))
            self._proto_name = proto.lower()

        def recv(id, args):
            if id == -1:
                callback(None, args)
                return
            if self._proto == None:
                if id == 255:
                    if len(args) != 1:
                        self._logger.warning("invalid arguments count for id %d" %id)
                        return
                    board = args[0]
                    for proto_name in self._protos:
                        proto = self._protos[proto_name]
                        if proto["id"] == board:
                            self._proto = proto
                            self._proto_name = proto_name.lower()
                            self.logger.info("Loading proto '%s'" %proto_name)
                            recv(id, args)
                    if self._proto == None:
                        self._logger.warning("unknow board %d" %board)
                else:
                    self._logger.info("no protocol loaded, can't decode id %d" %id)
            else:
                know_packet = False
                for packet_name in self._proto['packets']:
                    packet = self._proto['packets'][packet_name]
                    if packet['id'] == id:
                        know_packet = True
                        break
                if not know_packet:
                    self._logger.warning("unknow packet id %d" %id)
                    return
                if packet['transmitter'] == transmitter and packet['transmitter'] != 'both' and transmitter != 'both':
                    self._logger.info("ignoring %s message" %packet['transmitter'])
                    return
                if len(packet['args']) != len(args) \
                        and len(packet['args']) + 2 != len(args):
                    self._logger.warning("packet with id %d expected " \
                            "%d arguments, %d was given"
                            %(id, len(packet['args']), len(args)))
                    return
                arguments = dict(zip(packet['args'], args))
                if len(args) == len(packet['args']) + 2:
                    arguments['timestamp'] = args[-2]
                    arguments['microseconds'] = args[-1]
                if self._symmetrical:
                    symmetrical(self._proto_name, packet_name, arguments)
                callback(packet_name, arguments)

        thread = decode(stream, recv, follow)

    def _create_method(self, name, packet):
        def send(*args):
            if len(args) == len(packet['args']):
                self.send(name, packet, *args)
            else:
                self._logger.warning("'%s' expects %d arguments, %d given" \
                        ", packet not sended !"
                        %(name, len(packet['args']), len(args)))
        return send

    def send(self, name, packet, *args):
        if self._symmetrical:
            namedArgs = dict()
            names = list(packet['args'])
            for i in range(len(args)):
                namedArgs[names[i]] = args[i]
            symmetrical(self._proto_name, name, namedArgs)
            args = list(map(lambda x: namedArgs[x], namedArgs))
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
    parser.add_argument('-f', '--follow', dest='follow', action='store_true', help='output appended data as the file grows')
    parser.add_argument('-i', '--ipython', dest='ipython', action='store_true', help='launch ipython shell (need -c)')
    parser.add_argument('-s', '--symmetrical', dest='symmetrical', action='store_true', help='symmetrical packets')
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

    if args.connect and args.ipython:
        callback = lambda x, y: None
    else:
        callback = print_packet

    channel = Channel(stream, callback, proto = args.proto, transmitter = 'both',
        follow = args.follow, symmetrical = args.symmetrical)

    if args.connect and args.ipython:
        from IPython import embed
        embed()
