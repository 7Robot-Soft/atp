from atp import encode, decode
from threading import Thread, Event
import sys
from packet import Packet
from protos import Proto

class Channel:
    
    def __init__(self, protoDef, stream, callback, genAll = False):
        
        Thread.__init__(self)
        self._running = Event()

        #self._socket = socket
        #self._file = socket.makefile(mode="rw").buffer
        self._file  = stream
        self._callback = callback
        self._thread = Thread(target=decode, args=(self._file, self._recv))
        self._desc = {}

        self.parseProto(protoDef, genAll)
        if issubclass(protoDef, Proto):
            self.parseProto(Proto)

        self._thread.start()

    def parseProto(self, protoDef, genAll = False):
        for attrn in protoDef.__dict__:
            attr = protoDef.__getattribute__(protoDef, attrn)
            if isinstance(attr, Packet):
                if attrn in self.__dict__:
                    print("Warning: '%s' is a reserved packet name, ignoring" %attrn,
                            file=sys.stderr)
                else:
                    if attr.direction == "pic" or attr.direction == "both" \
                            or genAll:
                        attr.name = attrn
                        self._desc[attr.id] = attr
                    if attr.direction == "arm" or attr.direction == "both" \
                            or genAll:
                        self.__setattr__(attrn, self._create_send(attrn, attr))

    def _create_send(self, name, desc):
        def send(*args):
            self._send(name, desc, *args)
        return send

    def _send(self, name, desc, *args):
        formats = list(map(lambda x: x[1], desc.attrs))
        encode(self._file, desc.id, list(zip(args, formats)))

    def _recv(self, id, args):
        if id not in self._desc:
            print("Warning: ignoring unknow packet (id = %d)" %id, file=sys.stderr)
            return
        if len(args) != len(self._desc[id].attrs):
            print("Warning: invalid arguments count for this id (id = %d)" %id, file=sys.stderr)
            return
        names = map(lambda x: x[0], self._desc[id].attrs)
        self._callback(self._desc[id].name, dict(zip(names, args)))
