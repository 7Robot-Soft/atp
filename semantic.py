# Rappel des types struct.pack usuelles :
# B  unsigned char
# H  unsigned short
# I  unsigned int 
# b  signed char
# h  signed short
# i  signed int 
# f  float

from protos import Packet, Proto

# yymmjjhhmm
version = 1303020239

class Common(Proto):
    def __init__(self):
        print("Common")
        super(Common, self)

    test = Packet(252, "both", [
            ("B", "B"),
            ("H", "H"),
            ("I", "I"),
            ("b", "b"),
            ("h", "h"),
            ("i", "i"),
            ("f", "f")
        ])
    error = Packet(253, "pic")
    getId = Packet(254, "arm")
    id = Packet(255, "pic", [
            ("id", "B")
        ])

class Asserv(Proto):
    type = 5

    dist = Packet(10, "arm", [
            ("dist", "I")
        ])
    stop = Packet(11, "arm")
    done = Packet(12, "pic")

    getPos = Packet(20, "arm")
    pos = Packet(21, "pic", [
            ("x", "f"),
            ("y", "f")
        ])

    goTo = Packet(126, "arm", [
            ("x", "f"),
            ("y", "f"),
            ("theta", "f")
        ])

class Sensor(Proto):
    type = 2

    getValue = Packet(1, "arm", [
            ("id", "B")
        ])
    value = Packet(2, "pic", [
            ("id", "B"),
            ("value", "f")
        ])
    setThreshold = Packet(3, "arm", [
            ("id", "B"),
            ("threshold", "f")
        ])