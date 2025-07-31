#!/bin/bash
set -e

echo "Script coordinandor entre emisor <-> receptor por pipe!"

#Duplica la salida del receptor y la envía al emisor para que tenga el PID
./receptor.py | tee >(head -n1 | xargs ./emisor.py)