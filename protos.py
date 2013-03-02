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
