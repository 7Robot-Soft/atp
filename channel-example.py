#!/usr/bin/env python

from time import sleep
import socket
from channel import Channel
from protos import Captor

def print_packet(name, args): 
    print("[%s]" %name) 
    for k, v in args.items(): 
        print("\t", k, ":", v)

if __name__=="__main__":
    
    socket = socket.socket()
    socket.connect(("localhost", 1305))
   
    # Création du channel, en utilisant la norme « Captor », sur la socket
    # ouverte précédemment, et en appelant la fontion print_packet à la
    # réception d’un packet.
    captor = Channel(Captor, socket, print_packet)
    
    while True:
        ## On envoit de temps en temps un packet.
        captor.getValue(3)
        sleep(1)
        captor.getId()
        sleep(1)
