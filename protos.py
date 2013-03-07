#!/usr/bin/env python3

import inspect
from collections import OrderedDict

cformats = { 'B' : 'unsigned char',
            'H' : 'unsigned int',
            'I' : 'unsigned long int',
            'b' : 'char',
            'h' : 'int',
            'i' : 'long int',
            'f' : 'float' }

class Proto:
    pass

class Packet:
    def __init__(self, id, direction = "both", attrs = []):
        self.id = id
        if direction not in [ "pic", "arm", "both" ]:
            print("Warning: direction must be 'pic', 'arm' or 'both'. "
                "Assume 'both'.", file=sys.stderr)
            self.direction = "both"
        else:
            self.direction = direction
        self.attrs = attrs


def load(genAll = False):

    import semantic

    protos = OrderedDict()

    for name, proto in inspect.getmembers(semantic,
            lambda x: inspect.isclass(x) and issubclass(x, semantic.Proto)):
        if name != "Proto" and name != "Common":
            protos[name] = load_proto(proto, genAll)

    return protos

def load_proto(proto, genAll = False):

    import semantic

    p = OrderedDict()

    p['id'] = proto.type
    p['packets'] = OrderedDict()

    for name, packet in inspect.getmembers(semantic.Common,
            lambda x: isinstance(x, semantic.Packet)):
        p['packets'][name] = load_packet(packet, genAll)

    for name, packet in inspect.getmembers(proto,
            lambda x: isinstance(x, semantic.Packet)):
        p['packets'][name] = load_packet(packet, genAll)

    return p

def load_packet(packet, genAll = False):
    p = OrderedDict()

    p['id'] = packet.id
    if genAll:
        p['direction'] = 'both'
    else:
        p['direction'] = packet.direction
    p['args'] = OrderedDict()
    for arg, type in packet.attrs:
        p['args'][arg] = type

    return p

if __name__ == "__main__":
    protos = load()
    for proto in protos:
        p = protos[proto]
        print("%s: (board %d)" %(proto, p['id']))
        for packet in p['packets']:
            pa = p['packets'][packet]
            print("  [%3d, %4s] %s" %(pa['id'], pa['direction'], packet))
            for arg in pa['args']:
                format = pa['args'][arg]
                print("      %-10s \t(%s)" %(arg, cformats[format]))
