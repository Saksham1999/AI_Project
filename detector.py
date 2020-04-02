# importing required libraries
import cv2
import os
import numpy as np
from PIL import Image
import pickle
import sqlite3

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainner/trainner.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath) # Loading the xml file to detect faces
path="dataSet"

def getProfile(Id):
    conn = sqlite3.connect("FaceBase.db") # connecting with the database
    cmd = "SELECT *  FROM People WHERE ID="+str(Id) # fetching the row which matches the id from the database
    cursor = conn.execute(cmd)
    fetch_data = None
    for row in cursor:
        fetch_data = row
    conn.close() # closing the connection with the database
    return fetch_data


camera = cv2.VideoCapture(0) # turning on the device camera
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1.2
#fontcolor = (0, 255, 255)
while True:
    ret, image =camera.read() # capturing images to detect
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # converting the images into grayscale
    faces=faceCascade.detectMultiScale(gray, 1.2,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(225,0,0),2) # to draw rectangle on faces
        Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
        fetch_data = getProfile(Id) # calling the function with id as parameter to get the row which matches the id from the database
        if(fetch_data != None): # if the id matches with yhe id in database
            if(conf<80):
                cv2.putText(image, str(fetch_data[0]), (x, y + h+30), fontface, fontscale, (125,255,255),2,cv2.LINE_AA)
                cv2.putText(image, str(fetch_data[1]), (x, y + h+60), fontface, fontscale, (255,0,255),2,cv2.LINE_AA)
                cv2.putText(image, str(fetch_data[2]), (x, y + h+90), fontface, fontscale, (0,0,255),2,cv2.LINE_AA)
            else: # if id does not matches then do this
                cv2.putText(image, "New Face", (x, y + h + 60), fontface, fontscale, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow('image',image)
    cv2.waitKey(100) # wait for 100 milliseconds
camera.release()
cv2.destroyAllWindows()
