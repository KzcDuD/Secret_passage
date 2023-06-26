#!user/bin/python
import socket

ServerIP="127.0.0.1"
ServerPort=1234

# Establish socket
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect
s.connect((ServerIP,ServerPort))
print("Connect Establish!")

# Disconnect
s.close()