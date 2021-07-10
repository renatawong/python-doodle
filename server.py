from socket import *

# define socket object (for ipv4 and tcp protocol)
s = socket(AF_INET, SOCK_STREAM)

# bind the object (localhost as we do it on local machine, and port 1234)
s.bind((gethostname(), 1234))
# the server will listen to a queue of 5
s.listen(5)

# listening for connections
while True:
	clientsocket, address = s.accept()       # accepting all connection requests, clientsocket is another socket object
	print(f"Connection from {address} has been established!")
	clientsocket.send(bytes("Welcome to the server!", "utf-8"))   # sending information to clientsocket, bytes are of utf-8 form