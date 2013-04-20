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

class Demo(Proto):
    type = 1

    blinkOn = Packet(1, "arm")
    blinkOff = Packet(2, "arm")

    setDelay = Packet(3, "arm", [
            ("delay", "H")
        ])

    ledOn = Packet(4, "arm")
    ledOff = Packet(5, "arm")

    setCallback = Packet(6, "arm", [
            ("nbloop", "B")
        ])
    callback = Packet(7, "pic")


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

class Ax(Proto):
    type = 3

    GetPos = Packet(1, "arm", [
            ("idpic", "B")
        ])
    Pos = Packet(2, "pic", [
            ("id", "B"),
            ("value", "f")
        ])

    BougiesHitTop = Packet(3, "arm", [            
        ])
    BougiesHitTopConfirm = Packet(4, "pic", [            
        ])

    BougiesHitBot = Packet(5, "arm", [            
        ])
    BougiesHitBotConfirm = Packet(6, "pic", [            
        ])

    BougiesOff = Packet(7, "arm", [            
        ])
    BougiesOffConfirm = Packet(8, "pic", [            
        ])

    BougiesOn = Packet(9, "arm", [            
        ])
    BougiesOnConfirm = Packet(10, "pic", [            
        ])

    VerresEnd = Packet(11, "arm", [            
        ])
    VerresEndConfirm = Packet(12, "pic", [            
        ])

    VerresCatch = Packet(13, "arm", [            
        ])
    VerresCatchConfirm = Packet(14, "pic", [            
        ])

    VerresOff = Packet(15, "arm", [            
        ])
    VerresOffConfirm = Packet(16, "pic", [            
        ])

    VerresOn = Packet(17, "arm", [            
        ])
    VerresOnConfirm = Packet(18, "pic", [            
        ])

class Funny(Proto):
    type = 4

    FunnyAction = Packet(1, "arm", [
        ])
    EndFunnyAction = Packet(2, "pic", [
            ("id", "B")
        ])
    setThreshold = Packet(3, "arm", [
            ("id", "B"),
            ("threshold", "f")
        ])

# Rappel des types struct.pack usuelles :
# B  unsigned char
# H  unsigned short
# I  unsigned int 
# b  signed char
# h  signed short
# i  signed int 
# f  float
