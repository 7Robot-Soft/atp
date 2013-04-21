#!/usr/bin/bash

DEST=logs

TEXT_FIRST=1300
TEXT_LAST=1300

ATP_FIRST=1301
ATP_LAST=1305

HOST=$(grep HOST settings.py | cut -d'"' -f 2)

mkdir -p $DEST

for port in $(seq $TEXT_FIRST $TEXT_LAST); do 
    setsid nc -d $HOST $port </dev/null 2>/dev/null > "$DEST/$port.log" &
done
for port in $(seq $ATP_FIRST $ATP_LAST); do 
    setsid nc -d $HOST $port </dev/null 2>/dev/null | microstamp > "$DEST/$port.log" 2>/dev/null &
done
