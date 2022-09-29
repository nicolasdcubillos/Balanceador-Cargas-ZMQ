import sys
import zmq

port = "5556"

if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)
    
if len(sys.argv) > 2:
    port1 = sys.argv[2]
    int(port1)

context = zmq.Context()
socket = context.socket(zmq.SUB)

host = "tcp://localhost:" + port
print (f"[!] Iniciando balanceador de carga. \nIniciando conexión al servidor {host}")
socket.connect(host)

print ("Conexión exitosa.") # TODO: Try catch.

#   Para hacer conexión a más de un publicador

#if len(sys.argv) > 2:
#    socket.connect ("tcp://localhost:%s" % port1)
    
socket.setsockopt(zmq.SUBSCRIBE, b'')

while True:
    response = socket.recv().decode()
    print(response)