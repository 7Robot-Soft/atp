#-*- coding: utf-8 -*-

import struct
import sys

formats = { 1 : '<B', 2 : '<H', 4 : '<I', 17 : '<b', 18 : '<h', 20 : '<i', 36 : '<f' }

def encode(stream, id, args):
    stream.write(struct.pack('B', 129))
    stream.write(struct.pack('B', int(id)))
    for value, type in args:
        code = None
        for c, f in formats.items():
            if type == f[1]:
                code = c
                break
        if code == None:
            print("[proto] unknow type", file=sys.stderr)
            stream.write(struct.pack('B', 128))
            return
        if type == 'f':
            value = float(value)
        else:
            value = int(value)
        stream.write(struct.pack('B', code))
        stream.write(struct.pack('<'+type, value))
    stream.write(struct.pack('B', 128))
    

def decode(stream, callback):
    data = b''
    expected = 'begin'
    length = 1
    format = ''
    id = 0
    errors = 0
    args = []

    while True:
        c = stream.read(1)
        if not len(c):
            exit()
        data += c
        while len(data) >= length:
            if expected == 'begin':
                c = data[0]
                data = data[1:]
                if c == 129: # Début de trame
                    expected = 'id'
                else:
                    print('[proto] expected beginning flag (%d)' %c, file=sys.stderr)
                    errors += 1
            elif expected == 'id':
                c = data[0]
                data = data[1:]
                id = c
                args = []
                expected = 'type'
            elif expected == 'type':
                c = data[0]
                data = data[1:]
                if c == 128: # Fin de trame
                    callback(id, args)
                    expected = 'begin'
                else:
                    try:
                        format = formats[c]
                    except KeyError:
                        print('[proto] unknow format (%d), waiting next flag'
                                %c, file=sys.stderr)
                        errors += 1
                        expected = 'begin'
                    length = c & 0b1111
                    value = b''
                    expected = 'data'
            elif expected == 'data':
                value = struct.unpack(format, data[0:length])
                data = data[length:]
                args.append(value[0])
                expected = 'type'
                length = 1
