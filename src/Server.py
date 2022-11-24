import zmq
import sys
import bcrypt
import hashlib
import mysql.connector

cnx = mysql.connector.connect(
    user='root', password='Distribuidos2022', host='127.0.0.1', database='distributed')

contextResponse = zmq.Context()
socketResponse = contextResponse.socket(zmq.PUB)
responsePort = "557" + sys.argv[1]
socketResponse.bind("tcp://*:%s" % responsePort)

contextLB = zmq.Context()
socketLoadBalancer = contextLB.socket(zmq.SUB)
loadBalancerHost = "tcp://localhost:5561"
socketLoadBalancer.connect(loadBalancerHost)

print("Conexión exitosa.")

serverId = (sys.argv[1])

socketLoadBalancer.setsockopt(zmq.SUBSCRIBE, bytes(sys.argv[1], "utf-8"))


def Create(username, password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    cursor = cnx.cursor()
    sql = "INSERT into User(username, password, salt) VALUES (%s, %s, %s)"
    val = (username, hashed, salt)
    cursor.execute(sql, val)
    cnx.commit()
    return "create_successfull"


def Login (username, password):
    try:
        salt = bcrypt.gensalt()
        cursor = cnx.cursor()
        sql = "SELECT * FROM User WHERE username = %s AND password != %s"
        val = (username, password)
        cursor.execute(sql, val)
        records = cursor.fetchall()
        cnx.commit()
        for row in records:
            salt_stored = row[2]
            password_stored = row[1]
        password_hashed = bcrypt.hashpw(password.encode('utf-8'), bytes(salt_stored,'utf-8'))
        if (password_hashed.decode('utf-8') == password_stored):
            return "auth_successfull"
        else: 
            return "error"
    except:
        return "error"

def Buy (productName, quantity):
    quantity = int(quantity)
    if quantity > 0:
        cursor = cnx.cursor()
        sql = "SELECT * FROM Products WHERE nombreProducto = %s"
        val = (productName,)
        cursor.execute(sql, val)
        records = cursor.fetchall()
        cantidadF = 0
        for row in records:
            cantidadD = row[2]
        if cantidadD < quantity:
            print(cantidadD)
            return "error"
        else: 
            cantidadF = cantidadD-quantity
        if cantidadF > 0:
            disponibleF = 1
        else: 
            disponibleF = 0
        sql = "UPDATE Products SET disponible = %s, cantidadD = %s WHERE nombreProducto = %s"
        val = (disponibleF, cantidadF, productName)
        cursor.execute(sql, val)
        cnx.commit()
        return "buy_successfull"
    else: 
        return "error"

def Stock():
    cursor = cnx.cursor()
    sql = "SELECT * FROM Products"
    cursor.execute(sql)
    records = cursor.fetchall()
    print(records)
    return str(records)

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
        response = Buy(request[3], request[4])
    elif requestType == "Stock":
        response = Stock()
        
    socketResponse.send(bytes(response, 'utf-8'))