from socket import *

# define socket object (for ipv4 and tcp protocol)
s = socket(AF_INET, SOCK_STREAM)

# instead of binding (like the server case) this socket wants to connect to the server
s.connect((gethostname(), 1234))

# a tcp socket is a stream of data, so we need to specify a buffer size (size of data chunk) for receiving messages (here: 1024)
message = s.recv(1024)
print(message.decode("utf-8"))