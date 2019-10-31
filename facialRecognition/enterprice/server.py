# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 09:29:29 2019

    CLIENT                                      SERVER
                signin:username   
       ----------------------------------->
                yes|no
       <-----------------------------------
       if yes:
                struct(size,image)
       ----------------------------------->
                struct(size,image)
       ----------------------------------->
                ......
       ----------------------------------->
                      . . . . . . 
                struct(size,image)
       ----------------------------------->
                struct(0,"")
       ----------------------------------->
      client close           server close client                 

            
            login:username   
       ----------------------------------->
            struct(size,recognizer)
       <----------------------------------- 
       if size==0:
           not exist
       else:
           recv recognizer
           client verification 
       
            verify:ack|nack|fake
       ----------------------------------->
       client close     server disconn client     
            
@author: 19083
"""

import socket, select
import common as com
import os
import faceModelBuild as fmb
import cv2,pickle,struct

HOST = '192.168.1.209'
PORT = 6666

connected_clients_sockets = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

connected_clients_sockets.append(server_socket)
counter = 0
try:
    while True:
        read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])
        for sock in read_sockets:
            data = b''
            if sock == server_socket:
                sockfd, client_address = server_socket.accept()
                print("received client socket from: ",client_address)
                connected_clients_sockets.append(sockfd)
            else:
                try:
                    data += sock.recv(4096)
                    if data:
                        txt = data.decode("utf-8").strip()
                        name = ""
                        print("received",txt)
                        if "signin" in txt:
                            _,name = txt.split(':')
                            msg = com.findkey(name)
                            print("send out: ",msg)
                            sock.sendall(msg.encode('utf-8'))
                        elif "image" in txt:
                            _,name = txt.split(':')
                            sock.sendall(data)
                            print("send out ",repr(data))
                            folder = "person/"+name.lower()
                            if not os.path.exists(folder):
                                os.makedirs(folder)
                            counter = com.recvimages(sock,folder)
                            # build model and close socket
                            fmb.faceModelBuild(name)
                            sock.close()
                            connected_clients_sockets.remove(sock)
                        elif "login" in txt:
                            _,name = txt.split(':')
                            msg = com.findkey(name)
                            print("send out: ",msg)
                            sock.sendall(msg.encode('utf-8'))
                        elif "model" in txt:
                            _,name = txt.split(':')
                            filename = "person/%s.model.yml"%name
                            com.sendfile(sock,filename)
                            print("Sent model file:"+filename)
                        elif "verify" in txt:
                            _,verify = txt.split(':')
                            print(verify)
                except:
                    sock.close()
                    connected_clients_sockets.remove(sock)
                    continue
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    server_socket.close()
