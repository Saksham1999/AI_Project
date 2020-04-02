#importing required libraries
import cv2,os
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector= cv2.CascadeClassifier("haarcascade_frontalface_default.xml") #XML file to detect faces

path="dataSet"
def getImagesAndLabels(path):
    #getting the path of the folder  which contain all the sample images
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    #create empth face list
    faceSamples=[]
    #creating a list of empty ids
    Ids=[]
    #now iterarting through the the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #Loading the images and converting it into gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Converting the PIL images into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id associated with image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extracting the face from the sample images
        faces=detector.detectMultiScale(imageNp)
        #If a face is there then append that in the list as well as Id of it
        for (x,y,w,h) in faces:
            faceSamples.append(imageNp[y:y+h,x:x+w])
            Ids.append(Id)
    return faceSamples,Ids


faces,Ids = getImagesAndLabels('dataSet')
recognizer.train(faces, np.array(Ids))
recognizer.save('trainner/trainner.yml')
