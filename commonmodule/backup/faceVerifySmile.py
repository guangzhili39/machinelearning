# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 14:08:04 2019
@author: Guangzhi Li
when the function faceVerify() is called, the function will ask the user
to input the user login account:
    * if the login user name is not found on the server, then "name not found"
    will be returned
    * otherwise the user login has registred and a face recognition model has been built
    the function will load the yaml model and activate the device built in webcam
    * the webcam will capture the frames and using face recognition classifier to identify
    the face with the model.
    * randomly the function will ask the user to smile and 20 frames to classifier smile
    * if the face classifier did not recognize the user correctly, "unknow" is returned
    * if the smile classifier did not recongnize the smile face correctly, "fake user" is returned
    * otherwise the user name is returned.
"""

def faceVerify():
    import cv2
    import os
    import random
    import inputtextmodule as mytext
    
    name = mytext.getusername()
    folder = "person/"+name.lower()

    if not os.path.exists(folder):
        return("name not found")
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('person/'+name+'.model.yml')
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
    real = 0
    rand = 0
    totalmatch = 0
    totalreal = 0
    while count < 10:
    #capture frame by frame
        timer += 1
        ret,frame = webcam.read()
        if rand == 1:
            cv2.putText(frame,"Please smile",(50,50),font,1,(66,50,240),2)
    # face detection in gray not colore
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray,scaleFactor=1.1, minNeighbors=5)
        if len(faces) > 0: # every second 
            if timer%20 == 0:
                count += 1
                rand = random.randint(0,1)
                if match > 0:
                    totalmatch += 1
                    match = 0
                if real > 0:
                    totalreal += 1
                    real = 0;
            for (x,y,w,h) in faces:
                roi_gray = gray[y:y+h,x:x+w]
                roi_color= frame[y:y+h,x:x+w]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                _,conf = recognizer.predict(roi_gray)
                print(name,conf)
                threshold = 70
                if conf < threshold:
                    match += 1
                    cv2.putText(frame,name,(x,y-10),font,1,(200,0,0),3)
                    smiles = smile_detector.detectMultiScale(roi_gray, 1.8, 20)
                    smile = 0
                    for (sx, sy, sw, sh) in smiles:
                        smile = 1
                        cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)
                    if rand == smile:
                        real += 1
                else:
                    cv2.putText(frame,"unknown",(x,y-10),font,1,(66,50,240),2)
        cv2.imshow("Find You",frame)           
        if cv2.waitKey(10) & 0xff == ord('q'):                
            break
    
    webcam.release()                                  
    cv2.destroyAllWindows()     
    print(count)
    print(totalmatch)
    print(totalreal)
    if totalmatch != count:
        return ("unknow") 
    else:
        if totalreal != count:
            return('fake user')
        else:
            return(name)
    
if __name__=='__main__':
    ret = faceVerify()
    print(ret)
    