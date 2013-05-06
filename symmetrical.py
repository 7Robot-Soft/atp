def symmetrical(proto, name, args):

    if proto == "asserv":

        if name == "pos" or name == "setPos":
            args["x"] = - int(args["x"])
