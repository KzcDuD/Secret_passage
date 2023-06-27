#!/user/bin/python
import socket

Hostip="127.0.0.1"
Hostport=12345

# Establish Socket
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ipv4 / tcp
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

# Bind Address
s.bind((Hostip, Hostport))

# Service Start
s.listen()
print("Server Started.")
target,ip =s.accept()
print("Victim connect!")

# Disconnect
s.close()
