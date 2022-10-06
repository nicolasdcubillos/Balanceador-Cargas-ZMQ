import zmq
import random
import sys
import time

port = "5556"

if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

while True:
    message = "Bienvenido desde el balanceador de cargas."
    socket.send(bytes(message, 'utf-8'))
    time.sleep(1)