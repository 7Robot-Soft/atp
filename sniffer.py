#!/usr/bin/env python

from time import sleep
import socket
from channel import Channel, MPacket, Proto
from sys import argv, exit
import protos

def print_packet(name, args): 
    print("[%s]" %name) 
    for k, v in args.items(): 
        print("\t", k, ":", v)

def set_direction(cls):
    for attrn in cls.__dict__:
        attr = cls.__getattribute__(cls, attrn)
        if isinstance(attr, MPacket):
            attr.direction = "pic"

if __name__=="__main__":
    
    if len(argv) != 4:
        print("Usage: %s HOST PORT SEMANTIC" %argv[0])
        exit(1)

    try:
        port = int(argv[2])
    except ValueError:
        print("Error: '%s' is not a port number" %argv[2])
        exit(1)

    socket = socket.socket()
    socket.connect((argv[1], int(argv[2])))

    try:
        semName = argv[3][0].capitalize() + argv[3][1:]
        sem = getattr(protos, semName)
    except AttributeError:
        print("Error: no semantic found for '%s'" %argv[3])
        exit(1)

    set_direction(sem)
    set_direction(Proto)

    channel = Channel(sem, socket, print_packet)
