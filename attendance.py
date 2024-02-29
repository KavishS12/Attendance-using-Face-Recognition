import cv2 as cv
import numpy as np
import face_recognition
import os
from datetime import datetime
import sqlite3

path = "individuals"
images = []
classNames = [] 

lst = os.listdir(path)
#print(lst)  

for img in lst:
    currImg = cv.imread(f'{path}/{img}')
    images.append(currImg)
    classNames.append(os.path.splitext(img)[0])
print("Name of individuals : " + ",".join(classNames))

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance2(name):
    with open("attendance.csv",'r+') as file_handler:
        data = file_handler.readlines()
        nameList = []
        for line in data:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            t = datetime.now()
            dtString = t.strftime('%H:%M:%S')
            file_handler.writelines(f'\n{name},{dtString}')

conn = sqlite3.connect('students.db')
c = conn.cursor()

def markAttendance(nm):
    try:
        c.execute("UPDATE students SET present = 1 WHERE name = ?", (nm,))
        conn.commit()
        print("Attendance marked successfully.")
    except sqlite3.Error as e:
        print("Error marking attendance:", e)

encodeListKnown = findEncodings(images)
print("Encoding done")

cap = cv.VideoCapture(0)

while True:
    success,img = cap.read()
    imgSmall = cv.resize(img,(0,0),None,0.25,0.25)
    imgSmall = cv.cvtColor(imgSmall,cv.COLOR_BGR2RGB)

    facesCurrFrame = face_recognition.face_locations(imgSmall)
    encodeCurrFrame = face_recognition.face_encodings(imgSmall)

    for encodeFace,faceloc in zip(encodeCurrFrame,facesCurrFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace,tolerance=0.5)
        face_dist = face_recognition.face_distance(encodeListKnown,encodeFace)
        print(face_dist)
        matchIndex = np.argmin(face_dist) #get the individual with least face distance(if it exists)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1,x2,y2,x1 = faceloc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            # Draw a box around the face
            cv.rectangle(img,(x1,y1),(x2,y2),(0,255,0),thickness=2)
            # Draw a label conatining name below the face
            cv.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv.FILLED)
            cv.putText(img,name,(x1+6,y2-6),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
            markAttendance(name)
            markAttendance2(name)

    cv.imshow('Webcam',img)
    cv.waitKey(1)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break   

cap.release()
cv.destroyAllWindows()

conn.close()
