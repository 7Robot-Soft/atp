import binascii
import struct
import sys
import time
from threading import Thread

formats = { 1 : '<B', 2 : '<H', 4 : '<I', 17 : '<b', 18 : '<h', 20 : '<i', 36 : '<f' }

def async(fcnt):

    def run(*k, **kw):
        t = Thread(target=fcnt, args=k, kwargs=kw)
        t.start()
        return t

    return run

def encode(stream, id, args):
    buffer = bytearray()
    buffer += struct.pack('B', 129)
    buffer += struct.pack('B', int(id))
    for value, type in args:
        code = None
        for c, f in formats.items():
            if type == f[1]:
                code = c
                break
        if code == None:
            print("[atp.encode] unknow type, assuming unsigned char",
                    file=sys.stderr)
            buffer += struct.pack('B', 128)
            return
        if type == 'f':
            value = float(value)
        else:
            value = int(value)
        buffer += struct.pack('B', code)
        buffer += struct.pack('<'+type, value)
    buffer += struct.pack('B', 128)
    stream.write(buffer)
    stream.flush()

@async
def decode(stream, callback, follow = False):

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
            if follow:
                time.sleep(0.1)
                continue
            else:
                callback(-1, [])
                sys.exit()
        data += c
        while len(data) >= length:
            if expected == 'begin':
                c = data[0]
                data = data[1:]
                if c == 129: # Début de trame
                    expected = 'id'
                else:
                    print('[atp.decode] expected beginning flag (%d)' %c, file=sys.stderr)
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
                elif c == 132: # timestamp
                    format = formats[4]
                    length = c & 0b1111
                    value = b''
                    expected = 'data'
                elif c == 148: # microseconds
                    format = formats[4]
                    length = c & 0b1111
                    value = b''
                    expected = 'data'
                else:
                    try:
                        format = formats[c]
                    except KeyError:
                        print('[atp.decode] unknow format (%d), waiting next flag'
                                %c, file=sys.stderr)
                        errors += 1
                        expected = 'begin'
                    length = c & 0b1111
                    value = b''
                    expected = 'data'
            elif expected == 'data':
                try:
                    value = struct.unpack(format, data[0:length])
                except struct.error:
                    print("[atp.decode] struct.unpack exception, ignoring argument %s of format %s" % (binascii.hexlify(data[0:length]), format), file=sys.stderr)
                else:
                    args.append(value[0])
                finally:
                    data = data[length:]
                    expected = 'type'
                    length = 1
