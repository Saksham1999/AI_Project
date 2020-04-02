import cv2 # importing opencv library
import sqlite3 #import sqlite3 to connect with database
camera = cv2.VideoCapture(0) # capturing images from device camera
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def insertOrUpdate(Id,Name,Profession):
    conn = sqlite3.connect("FaceBase.db") # Connect with database
    cmd = "SELECT * FROM People WHERE ID="+str(Id) # command to check whether id already exists
    cursor = conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist = 1
    if(isRecordExist == 1): #check if the entered id already exists then update the database
        cmd="UPDATE People SET Name='"+str(Name)+"',Profession='"+str(Profession)+"' WHERE ID="+str(Id)
    else:
        cmd="INSERT  INTO People(ID,Name,Profession) Values("+str(Id)+",'"+str(Name)+"','"+str(Profession)+"')" # If new id is entered then enter the whole information into database
    conn.execute(cmd)
    conn.commit()
    conn.close() # close the connection with database
Id = input('enter your id:') # Take id as input from user it will act as primary key in database
name = input("Enter your name:") # Take name from user
profession = input("Enter your Profession:") # Take user's profession as input
insertOrUpdate(Id,name,profession # calling the function to check if the id already exist then update the database else enter it into the database
sampleimage = 0 # Initially number of images in the dataset for a particular id is zero
while (True):
    ret, image = camera.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # converting the images into grayscale
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces: #To find faces in image and draw rectangle on faces
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # incrementing number of images taken as sample
        sampleimage = sampleimage + 1
        # save the sample images into dataset folder
        cv2.imwrite("dataSet/User." + Id + '.' + str(sampleimage) + ".jpg", gray[y:y + h, x:x + w])

        cv2.imshow('frame', image)
    # wait for 100 miliseconds
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    # if the sample image count is more than 120 then break
    elif sampleimage > 120:
        break
camera.release() # release the camera
cv2.destroyAllWindows()
