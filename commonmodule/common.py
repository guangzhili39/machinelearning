# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 10:02:23 2019
CLIENT                                      SERVER
                signin:username\r\n   
       ----------------------------------->
                yes|no\r\n
       <----------------------------------- 
                file:filesize:filename\r\n
       ----------------------------------->
                file:filesize:filename\r\n
       <-----------------------------------
                file_data\r\n
       ----------------------------------->
                      . . . . . . 
                file:filesize:filename\r\n
       ----------------------------------->
                file:filesize:filename\r\n
       <-----------------------------------
                file_data\r\n
       ----------------------------------->
                disconnect\r\n
       ----------------------------------->
            server disconnects the client

            
            login:username\r\n   
       ----------------------------------->
            model:modelsize:modelname\r\n
       <----------------------------------- 
            model:modelsize\r\n
       ----------------------------------->
            model_data
       <-----------------------------------
                      . . . . . . 
            verify:ack|nack
       ----------------------------------->
            server disconnects the client     
@author: 19083
"""
import os
import struct
import pickle
import cv2
    
def recvall(sock, maxmsgLen):
    return sock.recv(maxmsgLen)

def generateimage(count=10):
    images = []
    import cv2
    
    number = 0
    #detect the faces
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')    
    #cv2.namedWindow("frame",cv2.WINDOW_AUTOSIZE) 
    #capture frame from camera
    webcam = cv2.VideoCapture(0)
    while (number < count):
        #capture frame by frame
        ret,frame = webcam.read()
        # face detection in gray not colore
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray,1.2,5)
        if len(faces) > 0: 
            for (x,y,w,h) in faces:
#                roi_gray = gray[y:y+h,x:x+w]
                roi_color = frame[y:y+h,x:x+w]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                images.append(roi_color)
                #color = (255,0,0) #BGR 0-255
                number += 1
            # display the resulting frame
        cv2.waitKey(40)
        cv2.imshow("take photos",frame) 
    
    webcam.release()
    cv2.destroyAllWindows()
    return images 
    
def faceVerify(recognizer,name):
    import cv2,time,dlib
    import random
    import pyttsx3
    import eyeCloseDetection as eye
    
    clf = "haarcascade_frontalface_default.xml"
    eyedat = "shape_predictor_68_face_landmarks.dat"
    face_detector = cv2.CascadeClassifier(clf)
#    smile_detector= cv2.CascadeClassifier(sml)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(eyedat)      

#capture frame from camera
    webcam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    count = 0
    match = 0
    totalconf = 0
    during = 20
    rand = random.randint(0,20)
    print(rand)
    challenge = 0
    while count < 40:
        #capture frame by frame
        ret,frame = webcam.read()
        # face detection in gray not colore
        if count >=rand and count <= rand+during:
            if challenge == 0:
                engine = pyttsx3.init()
                engine.say("please close eyes for 3 seconds only")
                engine.runAndWait()
                challenge = 1
                
            cv2.putText(frame,"please close eyes",(20,20),font,1,(0,255,0),3)
        time.sleep(0.01)    

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray,1.1,5)
#        smiles = smile_detector.detectMultiScale(gray,1.8,20)
#        smiles = smile_detector.detectMultiScale(gray,1.8,20,
#                                                 flags=cv2.CASCADE_SCALE_IMAGE)
        if len(faces) > 0:
            count += 1
            for (x,y,w,h) in faces:
                roi_gray = gray[y:y+h,x:x+w]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                _,conf = recognizer.predict(roi_gray)
                totalconf += conf 
                threshold = 65
                if conf < threshold:
                    cv2.putText(frame,name,(x,y-10),font,1,(200,0,0),3)
                eyeclose,ear = eye.eyeCloseDetection(frame,detector,predictor)
                if count > rand and count <= rand+during:
                    match += eyeclose
#                if len(smiles) > 0:
#                    for (sx,sy,sw,sh) in smiles:
#                        roi_gray = gray[sy:sy+sh,sx:sx+sw]
#                        cv2.rectangle(frame, (sx, sy), (sx+sw, sy+sh), (0, 255, 0), 2)
#                    if count > rand and count <= rand+during:
#                        match += 1
#                    else:
#                        match -= 1
        cv2.imshow("Find You",frame)           
        if cv2.waitKey(50)&0xFF==27:
            break
    
    if totalconf/count > threshold:
        name = "unknow" 
    elif match <= 0:
        name = "fake"
    
    webcam.release()
    cv2.destroyAllWindows()
    return name

def findkey(name):
    folder = "person/"+name.lower()
    if not os.path.exists(folder):
        return "no"
    else:
        return "yes"
 

def findvalue(name):
    modelname = "person/"+name.lower()+".model.yml"
    if not os.path.exists(modelname):
        return "none"
    else:
        return modelname
 
def sendimage(sock,image):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    _, frame = cv2.imencode('.jpg', image, encode_param)
    data = pickle.dumps(frame, 0)
    size = len(data)
    sock.sendall(struct.pack(">L",size) + data)
    print("image data sent:"+str(size))
    return size
        
def recvimages(sock,folder):
    data = b""
    payload_size = struct.calcsize(">L")
    count = 0
    while True:
        while len(data) < payload_size:
            data += sock.recv(4096)
        print("Recv bytes: {}".format(len(data)))
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        print("msg_size: {}".format(msg_size))
        if msg_size == 0:
            break
        while len(data) < msg_size:
            data += sock.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        filename = folder+"/%s.jpg"%count
        cv2.imwrite(filename,gray)
        cv2.waitKey(10)
        print("write image file")
        count += 1
    return count
  
def sendfile(sock,filename):
    if os.path.exists(filename):
        length = os.path.getsize(filename)
#        print("write file size:"+length)
        sock.sendall(struct.pack(">L",length))
#        sock.send(convert_to_bytes(length)) # has to be 4 bytes
        with open(filename, 'rb') as infile:
            d = infile.read(2048)
            while d:
                sock.send(d)
                d = infile.read(2048)
        infile.close()
        print("read file from "+filename)
    
def recvfile(sock,filename):
    size = sock.recv(4)
    size = struct.unpack(">L", size)[0]
#    size = bytes_to_number(size)
#    print("file size:"+size)
    buffer = b''
    recvsize = 0
    while recvsize < size:
        data = sock.recv(2048)
        if not data:
            break
        if len(data)+recvsize > size:
            data = data[:size-recvsize]
        buffer += data
        recvsize += len(data)
    with open(filename,'wb') as f:
        f.write(buffer)
    f.close()
    print("read file size:",recvsize)

def convert_to_bytes(no):
    result = bytearray()
    result.append(no & 255)
    for i in range(3):
        no = no >> 8
        result.append(no & 255)
    return result

def bytes_to_number(b):
    res = 0
    for i in range(4):
        res += b[i] << (i*8)
    return res 