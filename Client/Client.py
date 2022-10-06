import zmq
import sys

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REQ)
sock.connect("tcp://localhost:5555")

# Send a "message" using the socket
sock.send(b"Hola desde cliente.")
print (sock.recv())