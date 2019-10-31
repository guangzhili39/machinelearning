# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 09:57:12 2019
CLIENT                                      SERVER
                signin:username   
       ----------------------------------->
                yes|no
       <----------------------------------- 
                image:username
       ----------------------------------->
                image:username
       <-----------------------------------
                      . . . . . . 
                image:size+data
       ----------------------------------->
                done
       ----------------------------------->
       client close     server disconn client

            
            login:username   
       ----------------------------------->
            model:size+data
       <----------------------------------- 
                      . . . . . . 
            verify:ack|nack|fake
       ----------------------------------->
       client close     server disconn client     

@author: 19083
"""

import socket
import common as com
import time,struct
import cv2

HOST = '192.168.1.209'
PORT = 6666

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
sock.connect(server_address)

def signin(sock, name):
    msg = 'signin:%s' % name
    sock.sendall(msg.encode('utf-8'))
    data = com.recvall(sock, 4096)
    if data:
        txt = data.decode('utf-8').strip()
        print(txt)
        if txt == 'yes':
            print(name+" already registrated")
        else:
            msg = 'image:%s' % name
            sock.sendall(msg.encode('utf-8'))
            data = com.recvall(sock, 4096)
            if data:
                images = com.generateimage(10)
                for image in images:
                    com.sendimage(sock,image)
                    print("send image to sock")
                    time.sleep(0.01)
                sock.sendall(struct.pack(">L",0))  
#            msg = 'done:%s' % name
#            sock.sendall(msg.encode('utf-8'))       
    return "ok"

def login(sock,name):
    msg = 'login:%s' % name
    sock.sendall(msg.encode('utf-8'))
    data = com.recvall(sock, 4096)
    if data:
        txt = data.decode('utf-8').strip()
        print(txt)
        if txt == "no":
            print("user:"+name+"not exist")
        else:
            msg = 'model:%s' % name
            sock.sendall(msg.encode('utf-8'))
            print("send model request")
            com.recvfile(sock,"tmp.yml")
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read('tmp.yml')
            answer = com.faceVerify(recognizer,name)
            msg = '%s' % answer
            sock.sendall(msg.encode('utf-8'))
    return "success"
                
if __name__ == '__main__':
    import loginModule as ac
    action,name=ac.getusername()
    ret =""
    if action == 'login':
        try:
            ret = login(sock,name)
            print(ret)
        except:
            print("login failed")
    elif action == 'signin':
        try:
            ret = signin(sock,name)
            print(ret)
        except:
            print("signin failed")
    sock.close()
            