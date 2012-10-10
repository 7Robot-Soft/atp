#!/usr/bin/python
#-*- coding: utf-8 -*-

from atp import encode
import sys

if len(sys.argv) < 2:
    print('Usage: [id] [type|value] [type|value] …', file=sys.stderr)
    exit()

encode(sys.stdout.buffer, sys.argv[1],
        list(map(lambda x: x.split('@'), sys.argv[2:])))
