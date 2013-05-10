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
version = 1305100635

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

    free = Packet(0, "arm")
    stop = Packet(1, "arm")
    resume = Packet(2, "arm")
    done = Packet(3, "pic")
    modes = Packet(4, "pic", [
            ("point", "h"),
            ("distance", "h"),
            ("angle", "h"),
            ("vitesse", "h"),
            ("omega", "h")
        ])
    infos = Packet(5, "pic", [
            ("distance", "f"),
            ("angle", "f"),
            ("vitesse", "f"),
            ("omega", "f")
        ])

    # Odométrie
    odoBroadcastOn = Packet(10, "arm")
    odoBroadcastOff = Packet(11, "arm")
    odoBroadcastSetDelay = Packet(12, "arm", [
            ("delay", "H")
        ])
    # Étalonage de l’odométrie
    setOdoXTheta = Packet(15, "arm", [
            ("x", "f"),
            ("theta", "f")
        ])
    setOdoYTheta = Packet(16, "arm", [
            ("y", "f"),
            ("theta", "f")
        ])
    setOdoXY = Packet(17, "arm", [
            ("x", "f"),
            ("y", "f")
        ])
    setOdoTheta = Packet(18, "arm", [
            ("theta", "f")
        ])
    setOdoXYTheta = Packet(19, "arm", [
            ("x", "f"),
            ("y", "f"),
            ("theta", "f")
        ])

    # Consigne de distance
    setDist = Packet(20, "arm", [
            ("dist", "f")
        ])
    setDistRampe = Packet(21, "arm", [
            ("dist", "f")
        ])

    # Consigne de position
    setPos = Packet(30, "arm", [
            ("x", "f"),
            ("y", "f"),
        ])
    getPos = Packet(31, "arm")
    pos = Packet(32, "pic", [
            ("x", "f"),
            ("y", "f"),
            ("theta", "f"),
        ])

    # Consigne de position angulaire
    setAngle = Packet(40, "arm", [
            ("theta", "f"),
        ])
    getAngle = Packet(41, "arm")
    angle = Packet(42, "pic", [
            ("theta", "f"),
        ])
    setAngleRampe = Packet(43, "arm", [
            ("theta", "f"),
        ])

    # Consigne de vitesse linéaire
    setVit = Packet(50, "arm", [
            ("v", "f"),
        ])
    getVit = Packet(51, "arm")
    vit = Packet(52, "pic", [
            ("v", "f"),
        ])

    # Consigne de vitesse de rotation
    setOmega = Packet(60, "arm", [
            ("omega", "f"),
        ])
    getOmega = Packet(61, "arm")
    omega = Packet(62, "pic", [
            ("omega", "f"),
        ])

    # Vitesses
    setCourbe = Packet(70, "arm", [
            ("v", "f"),
            ("omega", "f"),
        ])
    getCourbe = Packet(71, "arm")
    courbe = Packet(72, "pic", [
            ("v", "f"),
            ("omega", "f"),
        ])

    # Coefs asserv vitesse linéaire
    setAsservV = Packet(100, "arm", [
            ("KPv", "f"),
            ("KIv", "f"),
            ("KDv", "f"),
        ])
    getAsservV = Packet(101, "arm")
    asservV = Packet(102, "pic", [
            ("KPv", "f"),
            ("KIv", "f"),
            ("KDv", "f"),
        ])

    # Coefs asserv vitesse angulaire
    setAsservO = Packet(110, "arm", [
            ("KPo", "f"),
            ("KIo", "f"),
            ("KDo", "f"),
        ])
    getAsservO = Packet(111, "arm")
    asservO = Packet(112, "pic", [
            ("KPo", "f"),
            ("KIo", "f"),
            ("KDo", "f"),
        ])

    # Coefs asserv position linéaire
    setAsservD = Packet(120, "arm", [
            ("KPd", "f"),
            ("KId", "f"),
            ("KDd", "f"),
        ])
    getAsservD = Packet(121, "arm")
    asservD = Packet(122, "pic", [
            ("KPd", "f"),
            ("KId", "f"),
            ("KDd", "f"),
        ])

    # Coefs asserv position angulaire
    setAsservT = Packet(130, "arm", [
            ("KPt", "f"),
            ("KIt", "f"),
            ("KDt", "f"),
        ])
    getAsservT = Packet(131, "arm")
    asservT = Packet(132, "pic", [
            ("KPt", "f"),
            ("KIt", "f"),
            ("KDt", "f"),
        ])

    # Coefs arrêts
    setEpsilons = Packet(136, "arm", [
            ("d", "f"),
            ("di", "f"),
            ("t", "f"),
            ("ti", "f")
        ])

    # Coefs accélération max et vitesse max
    setLimits = Packet(137, "arm", [
            ("accD", "f"),
            ("accT", "f"),
            ("vMax", "f"),
            ("oMax", "f")
        ])

    # Seuils termes intégraux
    setSeuils = Packet(139, "arm", [
            ("distance", "f"),
            ("angle", "f")
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

    # Points de contrôle d’une trajectoire
    addPoint = Packet(160, "arm", [
            ("x", "f"),
            ("y", "f")
        ])
    fullPoints = Packet(161, "pic")
    clearPoints = Packet(162, "arm")
    remaining = Packet(163, "pic", [
            ("n", "H")
        ])


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
