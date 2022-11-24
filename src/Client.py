import zmq
import random
import sys
import time
import os

if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

portLoadBalancer = "5553"
context = zmq.Context()
socket = context.socket(zmq.PUB)

socket.connect("tcp://127.0.0.1:" + portLoadBalancer)

id = random.randint(100, 999)

contextServerResponse = zmq.Context()
socketLoadBalancerResponse = contextServerResponse.socket(zmq.SUB)
socketLoadBalancerResponse.connect("tcp://127.0.0.1:5590") # Por donde recibe las respuestas de los servidores.
socketLoadBalancerResponse.setsockopt(zmq.SUBSCRIBE, b'')

poller = zmq.Poller()
poller.register(socketLoadBalancerResponse, zmq.POLLIN)

def processResponse(request, response):
    global logged
    if request == "Login":
        if response[1] == "auth_successfull":
            logged = True
            return ("Auth successfully. Welcome to the store!")
        else:
            return ("Credentials error. Check the input data again.")
            
    elif request == "Create":
        if response[1] == "create_successfull":
            return ("Account created successfully!")
        else:
            return ("An error occurred creating the account. Check the input data again.")
            
    elif request == "Stock":
        stock = ""
        for item in range(1, len(response) - 1):
            stock += "ID: " + str(item) + " | " + response[item] + " - " + " Quantity: " + response[item + 1] + "\n"
        return stock
            
    elif request == "Buy":
        if response[1] == "buy_successfull":
            return ("Successful purchase!")
        else:
            return ("An error occurred in the purchase. Check the input data again.")
        

print (f"Client ID {id} starting:\n")

logged = False

def menu():
    global logged
    if not logged:
        print("1. Login")
        print("2. Create an account")
    else:
        print("A. Show stock.")
        print("B. Buy product.")
        print("C. Logout.")
    
    option = input("Choose an option: ")
    return option

while True:
    os.system('cls')
    print(f"Welcome to the store! (Client ID: {id})")
    
    option = menu()
    
    if option == "1":
        typeRequest = "Login"
        username = input("Username: ")
        password = input("Password: ")
        request = typeRequest + " " + username + " " + password
        
    elif option == "2":
        typeRequest = "Create"
        username = input("Username: ")
        password = input("Password: ")
        request = typeRequest + " " + username + " " + password

    elif option == "A":
        typeRequest = "Stock"
        request = typeRequest
        
    elif option == "B":
        typeRequest = "Buy"
        productName = input("Product name: ")
        quantity = input("Quantity: ")
        request = typeRequest + " " + productName + " " + quantity
        
    elif option == "C":
        logged = False
        continue
    
    #print(f"Petición '{request}' enviada al servidor.")
    socket.send(b"%d %s" % (id, bytes(request, 'utf-8')))
    
    socks = dict(poller.poll(30000))
    
    Failure = True
    
    if socks:
        if socks.get(socketLoadBalancerResponse) == zmq.POLLIN:
            response = socketLoadBalancerResponse.recv().decode().split()
            Failure = False
        
    if Failure == True:
        print(f"   Store timeout! Try it again :(")
        time.sleep(2)
    else:
        print(f"   -> {processResponse(typeRequest, response)}")
    
    input("\nPress enter to continue...")