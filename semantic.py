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
version = 1305100726

class Common(Proto):
    def __init__(self):
        print("Common")
        super(Common, self)

    test = Packet(250, "both", [
            ("B", "B"),
            ("H", "H"),
            ("I", "I"),
            ("b", "b"),
            ("h", "h"),
            ("i", "i"),
            ("f", "f")
        ])
    unknow = Packet(251, "pic")
    unimplemented = Packet(252, "pic")
    error = Packet(253, "pic")
    getId = Packet(254, "arm")
    id = Packet(255, "pic", [
            ("id", "B")
        ])

#class Demo(Proto):
#    type = 1
#
#    blinkOn = Packet(1, "arm")
#    blinkOff = Packet(2, "arm")
#
#    setDelay = Packet(3, "arm", [
#            ("delay", "H")
#        ])
#
#    ledOn = Packet(4, "arm")
#    ledOff = Packet(5, "arm")
#
#    setCallback = Packet(6, "arm", [
#            ("nbloop", "B")
#        ])
#    callback = Packet(7, "pic")


class Asserv(Proto):
    type = 5

    # Message de debug
    debugFloats = Packet(1, "pic", [
            ("x", "f"),
            ("y", "f"),
            ("t", "f")
        ])
    mode = Packet(2, "pic", [
            ("mode", "H")
        ])
    logRampe = Packet(3, "pic", [
            ("end", "f"),
            ("periode", "f"),
            ("vInit", "f"),
            ("vFin", "f"),
            ("vMax", "f"),
            ("aMax", "f"),
            ("dMax", "f"),
            ("speedIsMoreImportante", "h")
        ])

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

    setOdoTicByMeter = Packet(28, "arm", [
            ("tbm", "h")
        ])
    setOdoSpacing = Packet(29, "arm", [
            ("spacing", "f")
        ])

    # Demande de la position à l’odométrie
    getPos = Packet(30, "arm")
    pos = Packet(31, "pic", [
            ("x", "f"),
            ("y", "f"),
            ("theta", "f")
        ])

    # Asservissement
    stop = Packet(40, "arm")
    pause = Packet(41, "arm")
    resume = Packet(42, "arm")
    done = Packet(43, "pic")

    # Primitive de déplacement
    distSansRampe = Packet(50, "arm", [
            ("dist", "f")
        ])
    rotSansRampe = Packet(51, "arm", [
            ("rot", "f")
        ])
    cercleSansRampe = Packet(52, "arm", [
            ("speed", "f"),
            ("omega", "f")
        ])

    dist = Packet(53, "arm", [
            ("dist", "f")
        ])
    rot = Packet(54, "arm", [
            ("rot", "f")
        ])

    reachX = Packet(55, "arm", [
            ("x", "f")
        ])
    reachY = Packet(56, "arm", [
            ("y", "f")
        ])
    reachTheta = Packet(57, "arm", [
            ("theta", "f")
        ])
    reachXY = Packet(58, "arm", [
            ("x", "f"),
            ("y", "f")
        ])

    speed = Packet(60, "arm", [
            ("speed", "f")
        ])
    omega = Packet(61, "arm", [
            ("omega", "f")
        ])
    speedSansRampe = Packet(62, "arm", [
            ("speed", "f")
        ])
    omegaSansRampe = Packet(63, "arm", [
            ("omega", "f")
        ])
    cercle= Packet(64, "arm", [
            ("rayon", "f"),
            ("speed", "f")
        ])
    arcCercle= Packet(65, "arm", [
            ("rayon", "f"),
            ("theta", "f")
        ])
    cercleSansRampe = Packet(66, "arm", [
            ("rayon", "f"),
            ("speed", "f")
        ])
    arcCercleSansRampe = Packet(67, "arm", [
            ("rayon", "f"),
            ("theta", "f")
        ])

    # Paramètres
    setDistLimits = Packet(70, "arm", [
            ("vMax", "f"),
            ("aMax", "f"),
            ("dMax", "f")
        ])
    setRotLimits = Packet(71, "arm", [
            ("vMax", "f"),
            ("aMax", "f"),
            ("dMax", "f")
        ])

    setEpsilons = Packet(72, "arm", [
            ("Ed", "f"),
            ("Ev", "f"),
            ("Et", "f"),
            ("Eo", "f")
        ])

    setDeltaCoefs = Packet(73, "arm", [
            ("P", "f"),
            ("I", "f"),
            ("D", "f")
        ])
    setAlphaCoefs = Packet(74, "arm", [
            ("P", "f"),
            ("I", "f"),
            ("D", "f")
        ])


    # Back Bumper
    getBackBumperState = Packet(140, "arm")
    backBumperState = Packet(141, "pic", [
            ("state", "I"),
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
    SICKChangeOn = Packet(154, "arm")
    SICKChangeOff = Packet(155, "arm")


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
    StopFunnyAction = Packet(51, "arm")

    # AX12
    stopAX12 = Packet(60, "arm")
    startAX12 = Packet(61, "arm")
    getAX12Torque = Packet(62, "arm", [
            ("id", "B"),
            ("torque", "i"),
        ])
    AX12Torque = Packet(62, "pic", [
            ("id", "B"),
            ("torque", "i"),
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
