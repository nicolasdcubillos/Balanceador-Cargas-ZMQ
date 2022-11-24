import zmq
import sys
#import bcrypt
import hashlib
#import mysql.connector

#cnx = mysql.connector.connect(user='root', password='Distribuidos2022', host='127.0.0.1', database='distributed')

contextResponse = zmq.Context()
socketResponse = contextResponse.socket(zmq.PUB)
responsePort = "557" + sys.argv[1]
socketResponse.bind("tcp://*:%s" % responsePort)

contextLB = zmq.Context()
socketLoadBalancer = contextLB.socket(zmq.SUB)
loadBalancerHost = "tcp://localhost:5561"
socketLoadBalancer.connect(loadBalancerHost)

print ("Conexión exitosa.")

serverId = (sys.argv[1])
    
socketLoadBalancer.setsockopt(zmq.SUBSCRIBE, bytes(sys.argv[1], "utf-8"))

def Create(username, password):
    
    #salt = bcrypt.gensalt()
    #hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    #cursor = cnx.cursor()

    #sql = "INSERT into User(username, password) VALUES (%s, %s)"
    #val = (username, hashed)
    #cursor.execute(sql, val)

    #cnx.commit()
    return "create_successfull"

def Login (username, password):
    return "auth_successfull"

def Buy (productId):
    return "buy_successfull"

def Stock():
    return "Product1 Product2 Product3"

while True:
    request = socketLoadBalancer.recv().decode().split()
    clientId = request[1]
    requestType = request[2]
    print(f"[!] New request: Client ID {clientId} - Request type: {requestType}")
    
    if requestType == "Create":
        response = Create(request[3], request[4])
    elif requestType == "Login":
        response = Login(request[3], request[4])
    elif requestType == "Buy":
        response = Buy(request[3])
    elif requestType == "Stock":
        response = Stock()
        
    socketResponse.send(bytes(response, 'utf-8'))