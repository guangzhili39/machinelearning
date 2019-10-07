# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 16:57:46 2019

@author: 19083
"""

from flask import Flask, render_template
import cv2
import os
#import faceRecognition as fr
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('template.html')
@app.route('/my_login/')
def verify():
    def collect_labelname():
        label_dict = {}
        people = [person for person in os.listdir("person/")]
        for i,person in enumerate(people):
            label_dict[i] = person
        return (label_dict)

    label_dict = collect_labelname()
    label_match = {}
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('model.yml')
    clf = "cascades/data/haarcascade_frontalface_default.xml"
    face_detector = cv2.CascadeClassifier(clf)

#capture frame from camera
    webcam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    count = 0
    timer = 1
    while count < 10:
    #capture frame by frame
        timer += 1
        ret,frame = webcam.read()
    # face detection in gray not colore
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(
                gray,scaleFactor=1.1, 
                minNeighbors=5
                )
        if len(faces) > 0 and timer%20==0: # every second 
            count += 1
            for (x,y,w,h) in faces:
                roi_gray = gray[y:y+h,x:x+w]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                pred,conf = recognizer.predict(roi_gray)

                name = label_dict[pred].capitalize()
                print(name +" conf: "+ str(round(conf))) 
                threshold = 60
                if conf < threshold:
                    cv2.putText(frame,name,(x,y-10),font,1,(200,0,0),3)
                    if pred in label_match:
                        label_match[pred] +=1
                    else:
                        label_match[pred] = 1
                else:
                    cv2.putText(frame,"unknown",(x,y-10),font,1,(66,50,240),2)
    # display the resulting frame
#    cv2.putTEXT(frame,"ESC to Exit",(5,5),font,3,(66,53,240),2)
        cv2.imshow("Find You",frame)           
        if cv2.waitKey(40)&0xFF==27:
            break
    webcam.release()
    cv2.destroyAllWindows()
    
    name="unknow"
    for id in label_match:
        if label_match[id] > 5:
            name = label_dict[id]
            
    return render_template('template.html', name=name)

@app.route('/my_signin/')
def signin():
    import faceRegistration
    import faceRecognition
    
    faceRegistration.faceRegistration()
    faceRecognition.faceRecognition()
    
    return render_template('template.html',result="registered!")

if __name__=='__main__':
    app.run(debug=True)
