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
version = 1305091502

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

    # Odométrie
    odoBroadcastOn = Packet(10, "arm")
    odoBroadcastOff = Packet(11, "arm")
    odoBroadcastSetDelay = Packet(12, "arm", [
            ("delay", "H")
        ])
    # Étalonage de l’odométrie
    setOdoX = Packet(20, "arm", [
            ("x", "f")
        ])
    setOdoY = Packet(21, "arm", [
            ("y", "f")
        ])
    setOdoTheta = Packet(22, "arm", [
            ("theta", "f")
        ])
    setOdoXY = Packet(23, "arm", [
            ("x", "f"),
            ("y", "f")
        ])
    setOdoXTheta = Packet(24, "arm", [
            ("x", "f"),
            ("theta", "f")
        ])
    setOdoYTheta = Packet(25, "arm", [
            ("y", "f"),
            ("theta", "f")
        ])
    setOdoXYTheta = Packet(26, "arm", [
            ("x", "f"),
            ("y", "f"),
            ("theta", "f")
        ])


    # Back Bumper
    getBackBumperState = Packet(140, "arm")
    backBumperState = Packet(141, "pic", [
            ("state", "B"),
        ])

    # SICKs
    getSICKValue = Packet(150, "arm", [
            ("id", "B")
        ])
    SICKValue = Packet(151, "pic", [
            ("id", "B"),
            ("value", "B")
        ])
    SICKFloodOn = Packet(152, "arm")
    SICKFloodOff = Packet(153, "arm")


class Mother(Proto):
    type = 6

    # Pince pour les verres
    sortirPince = Packet(1, "arm")
    chopperVerre = Packet(2, "arm")
    lacherVerres = Packet(3, "arm")
    getNombreVerres = Packet(4, "arm")
    nombreVerres = Packet(5, "pic", [
            ("n", "H"),
        ])
    pasDeVerreEvent = Packet(6, "pic")

    # Bras pour les bougies
    BougiesHitTop = Packet(10, "arm")
    BougiesHitTopConfirm = Packet(11, "pic")

    BougiesHitBot = Packet(12, "arm")
    BougiesHitBotConfirm = Packet(13, "pic")

    BougiesOff = Packet(14, "arm")
    BougiesOffConfirm = Packet(15, "pic")

    BougiesOn = Packet(16, "arm")
    BougiesOnConfirm = Packet(17, "pic")

    # Arrêt d’urgence
    getEmergencyState = Packet(20, "arm")
    emergencyState = Packet(21, "pic", [
            ("emergency_state", "B"),
        ])

    # Trois switchs
    getSwitchOneState = Packet(30, "arm")
    switchOne = Packet(31, "pic", [
            ("state", "B"),
        ])
    getSwitchTwoState = Packet(32, "arm")
    switchTwo  = Packet(33, "pic", [
            ("state", "B"),
        ])
    getSwitchThreeState = Packet(34, "arm")
    switchThree  = Packet(35, "pic", [
            ("state", "B"),
        ])

    # Start Laisse
    getStartLaisseState = Packet(40, "arm")
    StartLaisseState = Packet(41, "pic", [
            ("state", "B"),
        ])

    # FunnyAction
    FunnyAction = Packet(50, "arm")
    EndFunnyAction = Packet(51, "pic")


# A supprimer, OK ?
class Buttons(Proto):
    type = 7
    ButtonAction = Packet(1, "pic", [
        ("id", "B"),
        ("state", "B") # open/close
    ])

class Turret(Proto):
    type = 8
    on = Packet(1, "arm")
    off = Packet(2, "arm")
    getPos = Packet(10, "arm", [
        ("id", "B")
    ])
    pos = Packet(11, "pic", [
        ("id", "B"),
        ("distance", "B"),
        ("angle", "B")
    ])


# Rappel des types struct.pack usuelles :
# B  unsigned char
# H  unsigned short
# I  unsigned int
# b  signed char
# h  signed short
# i  signed int
# f  float
