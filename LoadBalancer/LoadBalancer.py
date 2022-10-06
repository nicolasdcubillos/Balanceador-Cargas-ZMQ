import zmq
import random
import sys
import time


if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

portServer = "5555"
contextClient = zmq.Context()
socketClient = contextClient.socket(zmq.REP)
socketClient.bind("tcp://*:%s" % portServer)

portPublisher = "5556"
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % portPublisher)

while True:
    messageClient = socketClient.recv()
    socketClient.send(b"Respuesta desde el servidor")
    
    message = "Petición de cliente entrante."
    socket.send(bytes(message, 'utf-8'))
    time.sleep(1)