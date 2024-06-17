<h1>Attendance System using Face Reognition</h1>

<h3>Overview</h3>

This project aims to automate the attendance tracking process using face recognition technology. It utilizes OpenCV for image processing, face_recognition library for face detection and recognition, Streamlit for building the user interface, and SQLite for data storage. The system allows users to capture attendance by detecting faces through a webcam feed and records attendance data into a SQLite database. Additionally, it provides a user-friendly interface for viewing the attendance records.

<h3>Tools and Libraries Used</h3>

<b>OpenCV</b>: OpenCV is used for image processing tasks such as capturing frames from the webcam, detecting faces, and drawing bounding boxes around recognized faces.

<b>face_recognition</b>: The face_recognition library is employed for facial recognition tasks, including encoding faces, comparing faces, and identifying individuals from a database of known faces.

<b>Streamlit</b>: Streamlit is utilized to create a user-friendly web-based interface for the attendance system and provides an intuitive user experience.

<b>SQLite</b>: SQLite is employed as the database management system to store attendance records. It offers a lightweight and portable solution for managing structured data within the application.

<h3>Project Workflow</h3>

1.Images of individuals whose attendance needs to be tracked are stored in a directory named <b>"individuals"</b>. These images are used for encoding faces and training the face recognition model.

2.The images of individuals are processed to extract facial features using the <b>face_recognition library.</b> These features are then encoded into numerical representations that can be compared for recognition.

3.When the <b>"Taking Attendance"</b> page in the web app is accessed, the user is prompted to enter the date for which attendance is to be recorded.<br>
->Upon clicking the <b>"Capture attendance"</b> button, the system starts capturing frames from the webcam feed.For each frame, faces are detected and recognized using the pre-trained face recognition model.<br>
->If a recognized face is detected, the corresponding individual's name is displayed on the screen along with a green bounding box around the face.<br>
->The attendance for the recognized individual on the specified date is then marked in the SQLite database.

4.In the <b>"Displaying Attendance"</b> page, users can view the recorded attendance data.Upon clicking the <b>"Display Attendance"</b> button, the system retrieves attendance records from the SQLite database and displays them in tabular form.

<h3>Conclusion</h3>

The face recognition attendance system offers a modern and efficient solution for tracking attendance, reducing the administrative burden and improving accuracy. By leveraging the capabilities of OpenCV, face_recognition, Streamlit, and SQLite, the project provides a robust and user-friendly platform for attendance management.
