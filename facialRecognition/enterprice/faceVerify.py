# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 14:08:04 2019

@author: 19083
"""

def faceVerify(modelfile,name):
    import cv2
    import random
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(modelfile)
    clf = "haarcascade_frontalface_default.xml"
    sml = "haarcascade_smile.xml"
    face_detector = cv2.CascadeClassifier(clf)
    smile_detector= cv2.CascadeClassifier(sml)

#capture frame from camera
    webcam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    count = 0
    match = 0
    totalconf = 0
    during = 20
    rand = random.randint(0,20)
    print(rand)
    while count < 40:
        #capture frame by frame
        ret,frame = webcam.read()
        # face detection in gray not colore
        if count >=rand and count <= rand+during:
            cv2.putText(frame,"please smile",(20,20),font,1,(0,255,0),3)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray,1.1,5)
#        smiles = smile_detector.detectMultiScale(gray,1.8,20)
        smiles = smile_detector.detectMultiScale(gray,2.0,25)
        if len(faces) > 0:
            count += 1
            for (x,y,w,h) in faces:
                roi_gray = gray[y:y+h,x:x+w]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                _,conf = recognizer.predict(roi_gray)
                totalconf += conf 
                threshold = 60
                if conf < threshold:
                    cv2.putText(frame,name,(x,y-10),font,1,(200,0,0),3)
                if len(smiles) > 0:
                    for (sx,sy,sw,sh) in smiles:
                        roi_gray = gray[sy:sy+sh,sx:sx+sw]
                        cv2.rectangle(frame, (sx, sy), (sx+sw, sy+sh), (0, 255, 0), 2)
                    if count > rand and count <= rand+during:
                        match += 1
#                    else:
#                        match -= 1
        cv2.imshow("Find You",frame)           
        if cv2.waitKey(30)&0xFF==27:
            break
        
    if totalconf/count > threshold:
        name = "unknow" 
    elif match <= 0:
        name = "fake"
    
    webcam.release()
    cv2.destroyAllWindows()
    return name

if __name__== '__main__':
    ret = faceVerify(modelfile="person\guangzhi.model.yml",name='guangzhi')
    print(ret)