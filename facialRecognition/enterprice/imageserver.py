# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 19:35:05 2019

@author: 19083
"""

import socket
import cv2
import pickle,json
import struct ## new
import faceModelBuild as fmb

HOST='192.168.1.209'
PORT=6000

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')


conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        data += conn.recv(4096)
    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    if msg_size == 0:
        print("end of images")
        break
    else:
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        cv2.imshow('ImageWindow',frame)
        cv2.waitKey(1)

#model = fmb.faceModelBuild('guangzhi')   
with open("person/guangzhi.model.yml", "rb") as modelfile:
    data = modelfile.read()
size = len(data)
print("size: {}".format(size))
conn.sendall(struct.pack(">L", size) + data)
conn.close()
