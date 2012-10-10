#!/usr/bin/python
#-*- coding: utf-8 -*-

from atp import decode
import sys
import fcntl
import os


def print_packet(id, args):
    print("[%d]" %id)
    for i in args:
        print("\t", i)


decode(sys.stdin.buffer, print_packet)
