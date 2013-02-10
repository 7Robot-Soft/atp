# Rappel des types struct.pack usuelles :
# B  unsigned char
# H  unsigned short
# I  unsigned int 
# b  signed char
# h  signed short
# i  signed int 
# f  float

from channel import MPacket

class Asserv:
    type = 1

    dist = MPacket(10, "arm", [
            ("dist", "I")
        ])
    stop = MPacket(11, "arm")
    done = MPacket(12, "pic")

    getPos = MPacket(20, "arm")
    pos = MPacket(21, "pic", [
            ("x", "f"),
            ("y", "f")
        ])

    getId = MPacket(254, "arm")
    idAnswer = MPacket(255, "pic", [
            ("id", "I")
        ])
