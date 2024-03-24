import cv2 as cv
import numpy as np
import pandas as pd
import face_recognition
import os
import sqlite3
import streamlit as st

path = "individuals"
images = []
classNames = []

lst = os.listdir(path)

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

conn = sqlite3.connect('students.db')
c = conn.cursor()

def markAttendance(nm,date):
    try:
        sql_query = f"UPDATE students SET {date} = 1 WHERE name = ?"
        c.execute(sql_query, (nm,))
        conn.commit()
        print("Attendance marked successfully.")
    except sqlite3.Error as e:
        print("Error marking attendance:", e)

encodeListKnown = findEncodings(images)
print("Encoding done")

#date = input("Enter the date for which attendance is to be recorded :")

st.set_page_config(page_title="Attendance System",layout="centered")


st.sidebar.title('Navigation')
selected_page = st.sidebar.radio('Go to', ['Home Page','Taking Attendance', 'Displaying Attendance'])

if selected_page=='Home Page':
    with st.container():
        st.title("An Attendance project")
        st.text_input("Please Enter Your name")
        st.write("")
        st.text_input("Please Enter Your division")
        st.write("")

elif selected_page == 'Taking Attendance':
    st.header("Attendance taking portal")
    st.subheader("")
    st.write('---')

    date = st.text_input("Enter the date for which attendance is to be recorded:", "")
    date = "date_" + date


    with st.container():
        st.write('---')
        left_column, right_column = st.columns(2)
        with right_column:
            stop_button = st.button("Stop capturing")
        with left_column:
            button_pressed = st.button("Capture attendance")

            frame_placeholder = st.empty()

            if button_pressed and date:
                cap = cv.VideoCapture(0)

                while True:
                    success, img = cap.read()
                    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                    imgSmall = cv.resize(img, (0, 0), None, 0.25, 0.25)
                    imgSmall = cv.cvtColor(imgSmall, cv.COLOR_BGR2RGB)

                    facesCurrFrame = face_recognition.face_locations(imgSmall)
                    encodeCurrFrame = face_recognition.face_encodings(imgSmall)

                    for encodeFace, faceloc in zip(encodeCurrFrame, facesCurrFrame):
                        matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=0.5)
                        face_dist = face_recognition.face_distance(encodeListKnown, encodeFace)
                        print(face_dist)
                        matchIndex = np.argmin(face_dist)  # get the individual with least face distance(if it exists)

                        if matches[matchIndex]:
                            name = classNames[matchIndex].upper()
                            print(name)
                            y1, x2, y2, x1 = faceloc
                            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                            # Draw a box around the face
                            cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), thickness=2)
                            # Draw a label conatining name below the face
                            cv.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv.FILLED)
                            cv.putText(img, name, (x1 + 6, y2 - 6), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                            markAttendance(name, date)
                            # markAttendance2(name)
                    frame_placeholder.image(img)
                    # cv.imshow('Webcam',img)
                    cv.waitKey(1)

                    if stop_button:
                        frame_placeholder = st.empty()
                        break

                cap.release()
                cv.destroyAllWindows()

elif selected_page == 'Displaying Attendance':
    st.title("Welcome to the attendance portal")
    st.subheader("")
    st.write('---')
    st.write("")

    if st.button("Display Attendance"):
        st.text("Displaying Attendance")
        c.execute('SELECT * FROM students;')
        data = c.fetchall()
        column_names = [description[0] for description in c.description]
        st.write(pd.DataFrame(data, columns=column_names))

conn.close()