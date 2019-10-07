# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 09:53:58 2019

@author: 19083
"""
# face registration takes 10 faces of the user for training purposes
def faceRegistration():
    import numpy as np
    import cv2
    import os
    import inputtextmodule as mytext

    #detect the faces
    face_detector = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_default.xml')
    cv2.namedWindow("frame",cv2.WINDOW_AUTOSIZE)

    name = mytext.getusername()
    folder = "person/"+name.lower()
    print(folder)
    if not os.path.exists(folder):
        os.makedirs(folder)
        counter = 0
    else:
        print("you already registered")   
        counter = 10
    
    #capture frame from camera
    webcam = cv2.VideoCapture(0)
    timer = 1
    while (counter < 10):
        #capture frame by frame
        ret,frame = webcam.read()
        # face detection in gray not colore
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(
                gray,scaleFactor=1.2, 
                minNeighbors=5
                )
        if len(faces) > 0 and timer%10 == 0: # every second 
            for (x,y,w,h) in faces:
                roi_gray = gray[y:y+h,x:x+w]
                img_item = folder+'/'+str(counter)+".jpg"
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.imwrite(img_item,roi_gray)
                #color = (255,0,0) #BGR 0-255
                counter+=1
            # display the resulting frame
        timer +=1
        cv2.waitKey(40)
        cv2.imshow("take photos",frame) 
    
    webcam.release()
    cv2.destroyAllWindows()    