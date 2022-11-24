import zmq
import time

contextPub = zmq.Context()
socketServers = contextPub.socket(zmq.PUB)
publisherPort = "5561"
socketServers.bind("tcp://*:%s" % publisherPort)

contextServerResponse = zmq.Context()
socketServerResponse = contextServerResponse.socket(zmq.SUB)
socketServerResponse.connect("tcp://127.0.0.1:5571") # Por donde recibe las respuestas de los servidores.
socketServerResponse.connect("tcp://127.0.0.1:5572") # Por donde recibe las respuestas de los servidores.
socketServerResponse.connect("tcp://127.0.0.1:5573") # Por donde recibe las respuestas de los servidores.
socketServerResponse.connect("tcp://127.0.0.1:5574") # Por donde recibe las respuestas de los servidores.
socketServerResponse.connect("tcp://127.0.0.1:5575") # Por donde recibe las respuestas de los servidores.
socketServerResponse.setsockopt(zmq.SUBSCRIBE, b'')

contextClientResponse = zmq.Context()
socketClientResponse = contextPub.socket(zmq.PUB)
portClientResponse = "5590"
socketClientResponse.bind("tcp://*:%s" % portClientResponse)

poller = zmq.Poller()
poller.register(socketServerResponse, zmq.POLLIN)

contextSub = zmq.Context()
socketClients = contextSub.socket(zmq.SUB)
port = "5553"
socketClients.bind("tcp://*:%s" % port)
#socketClients.connect("tcp://127.0.0.1:5553") # Conexión al cliente.
socketClients.setsockopt(zmq.SUBSCRIBE, b'')

current = 0
max_servers = 3

def RoundRobin():
    global current
    current += 1
    if current == max_servers + 1:
        current = 1
    return current

while True:
    tokens = socketClients.recv().decode().split()
    print(f"\n[!] New request from client (ID: {tokens[0]}) \n   - Request type: {tokens[1]}\n   - Params:", end = " ")
    
    for index in range(2, len(tokens)):
        print(tokens[index], end = " ")
    
    print("")
    
    Failure = True
    
    while Failure:
        
        server = RoundRobin()
        
        request = str(server)
        
        for token in tokens:
            request += " " + token
        
        print(f"-> Routing to server #{server}.")
        socketServers.send(bytes(request, 'utf-8'))
        
        socks = dict(poller.poll(500))
        
        if socks:
            if socks.get(socketServerResponse) == zmq.POLLIN:
                serverResponse = socketServerResponse.recv().decode()
                serverResponse = tokens[0] + " " + serverResponse
                socketClientResponse.send(bytes(serverResponse, 'utf-8'))
                print(f"   Server response: {serverResponse}")
                Failure = False
        
        if Failure == True:
            print(f"   Server {server} timeout.")
            time.sleep(1)
    
    time.sleep(1)