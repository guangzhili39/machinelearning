# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 16:57:46 2019

@author: 19083
"""

import cv2
import os
#import faceRecognition as fr

def collect_labelname():
    label_dict = {}
    people = [person for person in os.listdir("person/")]
    for i,person in enumerate(people):
        label_dict[i] = person
    return (label_dict)

label_dict = collect_labelname()
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('model.yml')
clf = "cascades/data/haarcascade_frontalface_default.xml"
face_detector = cv2.CascadeClassifier(clf)

#capture frame from camera
webcam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    #capture frame by frame
    ret,frame = webcam.read()
    # face detection in gray not colore
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(
        gray,scaleFactor=1.2, 
        minNeighbors=5
    )
    if len(faces) > 0: # every second 
        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h,x:x+w]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            pred,conf = recognizer.predict(roi_gray)
            name = label_dict[pred].capitalize()
            print(name +" conf: "+ str(round(conf))) 
            threshold = 80
            if conf < threshold:
                cv2.putText(frame,name,(x,y-10),font,1,(200,0,0),3)
            else:
                cv2.putText(frame,"unknown",(x,y-10),font,1,(66,50,240),2)
    # display the resulting frame
#    cv2.putTEXT(frame,"ESC to Exit",(5,5),font,3,(66,53,240),2)
    cv2.imshow("Find You",frame)           
    if cv2.waitKey(40)&0xFF==27:
        break
    
webcam.release()
cv2.destroyAllWindows()

