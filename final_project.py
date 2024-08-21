import cv2 as cv
import numpy as np
import pandas as pd
import face_recognition
import os
import sqlite3
import streamlit as st

st.set_page_config(page_title="Attendance System", layout="centered")

# @st.cache_data  -  decorator provided by Streamlit for caching data within the app,
# helps improve performance by storing the results of expensive computations
# or data retrieval operations so that they do not need to be re-executed every time'''
@st.cache_data
def load_images_and_encodings(path):
    images = []
    classNames = []
    lst = os.listdir(path)
    for img in lst:
        currImg = cv.imread(f'{path}/{img}')
        images.append(currImg)
        classNames.append(os.path.splitext(img)[0])
    return images, classNames

@st.cache_resource
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(nm, date):
    try:
        sql_query = f"UPDATE students SET {date} = 1 WHERE name = ?"
        c.execute(sql_query, (nm,))
        conn.commit()
    except sqlite3.Error as e:
        print("Error marking attendance:", e)

# Load images and encodings once
path = "individuals"
images, classNames = load_images_and_encodings(path)
encodeListKnown = findEncodings(images)

# Setup Streamlit page
st.sidebar.title('Navigation')
selected_page = st.sidebar.radio('Go to', ['Home Page', 'Taking Attendance', 'Displaying Attendance'])

# Database connection
conn = sqlite3.connect('students.db')
c = conn.cursor()

if selected_page == 'Home Page':
    with st.container():
        st.title("An Attendance project")
        st.text_input("Please Enter Your name")
        st.write("")
        st.text_input("Please Enter Your division")
        st.write("")

elif selected_page == 'Taking Attendance':
    st.header("Attendance taking portal")
    st.write('---')

    date = st.text_input("Enter the date for which attendance is to be recorded(DD_MM) : ", "")
    date = "date_" + date
    c.execute(f"PRAGMA table_info(students);")
    columns = [row[1] for row in c.fetchall()]
    if date not in columns:
        try:
            c.execute(f"ALTER TABLE students ADD COLUMN {date} INTEGER DEFAULT 0;")
            conn.commit()
        except sqlite3.OperationalError as e:
            st.error(f"An error occurred: {e}")

    if 'capturing' not in st.session_state:
        st.session_state.capturing = False

    capture_button = st.button("Capture attendance", key="capture_button")
    frame_placeholder = st.empty()
    if capture_button and date:
        st.session_state.capturing = True
        frame_placeholder.info("Wait for a few seconds while the app loads the camera...")
    if st.session_state.capturing:
        stop_button = st.button("Stop capturing", key="stop_button")
        cap = cv.VideoCapture(0)
        while st.session_state.capturing:
            success, img = cap.read()
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            imgSmall = cv.resize(img, (0, 0), None, 0.25, 0.25)
            imgSmallRGB = cv.cvtColor(imgSmall, cv.COLOR_BGR2RGB)

            facesCurrFrame = face_recognition.face_locations(imgSmallRGB)
            encodeCurrFrame = face_recognition.face_encodings(imgSmallRGB)

            for encodeFace, faceloc in zip(encodeCurrFrame, facesCurrFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=0.5)
                face_dist = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(face_dist)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    y1, x2, y2, x1 = faceloc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    # Draw a box around the face
                    cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), thickness=2)
                    # Draw a label containing name below the face
                    cv.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv.FILLED)
                    cv.putText(img, name, (x1 + 6, y2 - 6), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    markAttendance(name, date)

            frame_placeholder.image(img)
            cv.waitKey(1)

            if stop_button:
                st.session_state.capturing = False
                frame_placeholder.success("Attendance captured.Click the \"Stop capturing\" button again to exit.")
                break

        cap.release()
        cv.destroyAllWindows()

elif selected_page == 'Displaying Attendance':
    st.title("Welcome to the attendance portal")
    st.subheader("")
    st.write('---')

    if st.button("Display Attendance", key="display_button"):
        c.execute('SELECT * FROM students;')
        data = c.fetchall()
        column_names = [description[0] for description in c.description]
        st.write(pd.DataFrame(data, columns=column_names))

conn.close()
