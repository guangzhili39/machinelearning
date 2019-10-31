# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 14:08:04 2019

@author: 19083
"""

def faceVerify():
    import cv2
    import os
    import inputtextmodule as mytext
    import types
    
    name = mytext.getusername()
    folder = "person/"+name.lower()

    if not os.path.exists(folder):
        return("name not found")
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('person/'+name+'.model.yml')
    print(types(recognizer))
    clf = "cascades/data/haarcascade_frontalface_default.xml"
    sml="cascades/data/haarcascade_smile.xml"
    face_detector = cv2.CascadeClassifier(clf)
    smile_detector= cv2.CascadeClassifier(sml)

#capture frame from camera
    webcam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    count = 0
    timer = 1
    match = 0
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
 
        if len(faces) > 0 and timer%10==0: # every second 
            count += 1
            for (x,y,w,h) in faces:
                roi_gray = gray[y:y+h,x:x+w]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                _,conf = recognizer.predict(roi_gray)
#                name = label_dict[pred].capitalize()
                print(name +" conf: "+ str(round(conf))) 
                threshold = 60
                if conf < threshold:
                    cv2.putText(frame,name,(x,y-10),font,1,(200,0,0),3)
                    match +=1
                else:
                    cv2.putText(frame,"unknown",(x,y-10),font,1,(66,50,240),2)
        cv2.imshow("Find You",frame)           
        if cv2.waitKey(10)&0xFF==27:
            break
    if match < 5:
        return ("unknow") 
        
    
## add challenge actions
    count = 0
    timer = 1
    match = 0
    while count < 10:
    #capture frame by frame
        timer += 1
        count += 1
        ret,frame = webcam.read()
        cv2.putText(frame,"Please smile",(50,50),font,1,(66,50,240),2)
    # face detection in gray not colore
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(
                gray,scaleFactor=1.1, 
                minNeighbors=5
                )
        smiles = smile_detector.detectMultiScale(
                gray,scaleFactor=1.1, 
                minNeighbors=5
                )
        if len(faces) > 0 and len(smiles)>0 and timer%10==0: # every second 
            for (x,y,w,h) in faces:
                roi_gray = gray[y:y+h,x:x+w]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                _,conf = recognizer.predict(roi_gray)

                threshold = 60
                if conf < threshold:
                    match +=1
        cv2.imshow("Find You",frame)           
        if cv2.waitKey(20)&0xFF==27:
            break
    if match == 0:
        return("fake")    

    webcam.release()
    cv2.destroyAllWindows()
    
    return(name)
    
if __name__=='__main__':
    ret = faceVerify()
    print(ret)