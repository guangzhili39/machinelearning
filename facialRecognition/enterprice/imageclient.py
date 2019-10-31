# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 19:32:33 2019

@author: 19083
"""

import cv2
import socket
import struct
import pickle
import json

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.209', 6000))
connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

cam.set(3, 320);
cam.set(4, 240);

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while img_counter < 30:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
#    data = zlib.compress(pickle.dumps(frame, 0))
    data = pickle.dumps(frame, 0)
    size = len(data)


    print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1
    
client_socket.sendall(struct.pack(">L",0))   
 
# receive the recognizer from server
data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))

while len(data) < payload_size:
    print("Recv: {}".format(len(data)))
    data += client_socket.recv(4096)

print("Done Recv: {}".format(len(data)))
packed_msg_size = data[:payload_size]
data = data[payload_size:]
msg_size = struct.unpack(">L", packed_msg_size)[0]
print("msg_size: {}".format(msg_size))
while len(data) < msg_size:
    data += client_socket.recv(4096)
frame_data = data[:msg_size]
data = data[msg_size:]
with open("tmp.yml", "wb") as newFile:
    newFile.write(frame_data)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('tmp.yml')

name,conf = recognizer.predict(frame)
print(name,conf)
client_socket.close()

cam.release()
