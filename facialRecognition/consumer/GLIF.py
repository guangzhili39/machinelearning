# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 09:57:12 2019
standalone facial recognition module for PC/laptop with webcam
features:
    1: user sign-in to capture images and build a model
    2: user login with live images plus challenge action
    3: user could use password to login
    
@author: 19083
"""

import common as com
import cv2
import os

def signin(name,cmdpath):
    import faceModelBuild as fmb
    
    folder = cmdpath+"/person/"+name.lower()
    if os.path.exists(folder):
        return "exist"
    else:
        os.makedirs(folder)
        
        images = com.generateimage(10,cmdpath)
        counter = 0
        for image in images:
            img_item = folder+"/"+str(counter)+".jpg"
            cv2.imwrite(img_item,image)
            counter += 1
        fmb.faceModelBuild(name)           
    return "success"

def login(name,cmdpath):
    
    folder = cmdpath+"/person/"+name.lower()+".model.yml"
    if not os.path.exists(folder):
        return "not exist"
    else:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(folder)
        answer = com.faceVerify(recognizer,name,cmdpath)
    return answer

def pwdlogin(name,cmdpath):
    
    folder = cmdpath+"/person/"+name.lower()+".pwd"
    pwd=""
    if not os.path.exists(folder):
        return "not exist"
    else:
        pwdfile = open(folder, "r")
        pwd = pwdfile.read()
        pwdfile.close() 
    return pwd
               
if __name__ == '__main__':
    import loginModule as ac
    import sys

    print(sys.argv[0])
    cmdpath = os.path.dirname(sys.argv[0])
    if cmdpath=='':
        cmdpath = '.'
    print(cmdpath)
    ret = " "
    while True:
        action,name,pwd = ac.getusername(ret)
        if action == 'login':
            ret = login(name,cmdpath)
        elif action == 'signin':
            if pwd.strip()=="":
                ret = "please input password during sign-in"
            else:
                filename=cmdpath+'/person/'+name.lower()+".pwd"
                if os.path.exists(filename):
                    ret = "user exits"
                else:
                    folder = cmdpath+'/person'
                    if not os.path.exists(folder):
                        os.mkdir(folder)
                    with open(filename,'w') as f:
                        f.write(pwd)
                        f.close()
                        ret = signin(name,cmdpath)
        elif action == 'pwdlogin':
            spwd = pwdlogin(name,cmdpath)
            if pwd == spwd:
                ret = name
            else:
                ret = "password does not match"
        if ret == name:
            break
           
#        if action == 'login':
#            try:
#                ret = login(name,cmdpath)
#                print(ret)
#            except:
#                print("login failed")
#        elif action == 'signin':
#            try:
#                ret = signin(name,cmdpath)
#                print(ret)
#            except:
#                print("signin failed")
#        elif action == 'pwdlogin':
#            if pwd == name+'123':
#                print(name)
#                break
#        if ret == name:
#            break