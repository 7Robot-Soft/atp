from atp import encode, decode
from threading import Thread, Event
import sys

class MPacket:
    
    def __init__(self, id, direction = "both", attrs = []):
        self.id = id
        if direction not in [ "pic", "arm", "both" ]:
            print("Warning: direction must be 'pic', 'arm' or 'both'. "
                "Assume 'both'.", file=sys.stderr)
            self.direction = "both"
        else:
            self.direction = direction
        self.attrs = attrs

class Channel:
    
    def __init__(self, protoDef, socket, callback):
        
        Thread.__init__(self)
        self._running = Event()

        self._socket = socket
        self._file = socket.makefile(mode="rw")
        self._callback = callback
        self._thread = Thread(target=decode, args=(self._file.buffer, self._recv))
        self._desc = {}

        for attrn in protoDef.__dict__:
            attr = protoDef.__getattribute__(protoDef, attrn)
            if isinstance(attr, MPacket): 
                if attrn in self.__dict__:
                    print("Warning: '%s' is a reserved packet name, ignoring" %attrn,
                            file=sys.stderr)
                else:
                    if attr.direction == "pic" or attr.direction == "both":
                        attr.name = attrn
                        self._desc[attr.id] = attr
                    if attr.direction == "arm" or attr.direction == "both":
                        self.__setattr__(attrn, self._create_send(attrn, attr))

        self._thread.start()

    def _create_send(self, name, desc):
        def send(*args):
            self._send(name, desc, *args)
        return send

    def _send(self, name, desc, *args):
        formats = list(map(lambda x: x[1], desc.attrs))
        encode(self._file.buffer, desc.id, list(zip(args, formats)))

    def _recv(self, id, args):
        if id not in self._desc:
            print("Warning: ignoring unknow packet (id = %d)" %id, file=sys.stderr)
            return
        if len(args) != len(self._desc[id].attrs):
            print("Warning: invalid arguments count for this id (id = %d)" %id, file=sys.stderr)
            return
        names = map(lambda x: x[0], self._desc[id].attrs)
        self._callback(self._desc[id].name, dict(zip(names, args)))
