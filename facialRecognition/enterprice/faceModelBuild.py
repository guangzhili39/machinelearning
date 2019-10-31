# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 09:53:58 2019

@author: 19083
"""
# face recognition 
# three types of models
# Eigen faces
#   cv2.face.createEigneFaceRecognizer()
# Fisher Faces
#   cv2.face.createFisherFaceRecognizer()
# LBPH faces
#   cv2.face.createLBPHFaceRecognizer()
def faceModelBuild(user):
    import numpy as np
    import cv2
    import os
    
    def collect_dataset(user):
        images=[]
        labels=[]
        people = [person for person in os.listdir("person/")]
        for i,person in enumerate(people):
            if user.lower() == person.lower():
                for image in os.listdir("person/"+person):
                    images.append(cv2.imread("person/"+person+'/'+image,0))
                    labels.append(0)
        return (images,np.array(labels))

    images,labels = collect_dataset(user)
    #rec_eig = cv2.face.EigenFaceRecognizer_create()
    #rec_eig.train(images,labels)
    #needs at least two people
    #rec_fisher = cv2.face.FisherFaceRecognizer_create()
    #rec_fisher.train(images,labels)

    rec_lbph = cv2.face.LBPHFaceRecognizer_create()
    
    rec_lbph.train(images,labels)
    rec_lbph.write("person/"+user+".model.yml") # print(dir(rec_lbph)) seems both .save and .write work
    return rec_lbph

if __name__=='__main__':
    rec = faceModelBuild('guangzhi')
    print("model built successfully")