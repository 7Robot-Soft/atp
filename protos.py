import semantic
import inspect
from collections import OrderedDict

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


def load():
    protos = OrderedDict()

    for name, proto in inspect.getmembers(semantic,
            lambda x: inspect.isclass(x) and issubclass(x, semantic.Proto)):
        if name != "Proto" and name != "Common":
            protos[name] = load_proto(proto)

    return protos

def load_proto(proto):
    p = OrderedDict()

    for name, packet in inspect.getmembers(semantic.Common,
            lambda x: isinstance(x, semantic.Packet)):
        p[name] = load_packet(packet)

    for name, packet in inspect.getmembers(proto,
            lambda x: isinstance(x, semantic.Packet)):
        p[name] = load_packet(packet)

    return p

def load_packet(packet):
    p = OrderedDict()

    p['id'] = packet.id
    p['direction'] = packet.direction
    for arg, type in packet.attrs:
        p[arg] = type

    return p
