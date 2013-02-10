# Rappel des types struct.pack usuelles :
# B  unsigned char
# H  unsigned short
# I  unsigned int 
# b  signed char
# h  signed short
# i  signed int 
# f  float

from channel import MPacket, Proto

class Asserv(Proto):
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

    goTo = MPacket(126, "arm", [
            ("x", "f"),
            ("y", "f"),
            ("theta", "f")
        ])
