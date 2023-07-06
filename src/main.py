import gspread
from oauth2client.service_account import ServiceAccountCredentials 

import face_recognition
import cv2
import numpy as np

import datetime
import os
import sys

sys.path.insert(1, "C:\\Users\\parent\\Desktop\\Coding\\Github\\project-showface-pw-2023")

scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]

file_name = 'client_key.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
client = gspread.authorize(creds)

spreadsheet = client.open('project_showface')
worksheet = spreadsheet.worksheet('Sheet1')

video_capture = cv2.VideoCapture(0)

# load images of the different faces to recognise them
known_faces = {}

img_paths = [i.path for i in os.scandir("img")]

for img in img_paths:
    name = img[4:-4]
    encoding = face_recognition.face_encodings(face_recognition.load_image_file(img))[0]
    known_faces[name] = encoding

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
capture = False

while True:
    # capture a video frame
    ret, frame = video_capture.read()

    # if the c button is pressed, this photo program will run
    if capture == True:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        # makes the file name
        name = input("Please enter your file name: ")
        #filename = f"captured_photo_{timestamp}.jpg"

        # Save the captured photo
        cv2.imwrite("img\\" + name + ".jpg", frame)

        print(f"Photo captured and saved")

        # allocates the photo to image variable
        image = face_recognition.load_image_file("img\\" + name + ".jpg")
        face_encoding = face_recognition.face_encodings(image)[0]

        #adds a new key to dictionary
        known_faces[name] = face_encoding

        print(f"Face for '{name}' added successfully.")

        capture = False

    if process_this_frame:
        # resize the video to 1/4 the size to save time
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # convert bgr (what opencv uses) to rgb (what facial_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        #find all the faces in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_location in face_locations:
            # check if the face matches any known face
            face_encoding = face_recognition.face_encodings(rgb_small_frame, [face_location])[0]
            matches = face_recognition.compare_faces(list(known_faces.values()), face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(list(known_faces.values()), face_encoding)
            best_match_index = np.argmin(face_distances)
            
            # if match found, find the name of the person
            if matches[best_match_index]:
                name = list(known_faces.keys())[best_match_index]

            # after match found, change attendance on google sheet
            if name != "Unknown":
                cell_list = worksheet.findall(name)
                if cell_list:
                    cell = cell_list[0]

                    # get row and col number of the cell
                    row_number = cell.row 
                    col_number = cell.col 

                    # get the current time
                    current_time = int(datetime.datetime.now().strftime("%H%M%S"))
                    formatted_time = str(current_time)[0:2] + ":" + str(current_time)[2:4] + ":" + str(current_time)[4:]
                    

                    # change the attendance correspondingly
                    if current_time > 80000:
                        worksheet.update_cell(row_number, col_number + 1, formatted_time)
                        worksheet.update_cell(row_number, col_number + 2, "Late")

                    else:
                        worksheet.update_cell(row_number, col_number + 1, formatted_time)
                        worksheet.update_cell(row_number, col_number + 2, "Present")

            face_names.append(name)

    process_this_frame = not process_this_frame

    # display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # rescale the video since it was resized to 1/4
        top *= 4
        left *= 4
        right *= 4
        bottom *= 4
        
        # draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # draw a label below the face with the name
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # display the resulting image
    cv2.imshow('Video', frame)

    # quit programme if 'q' is pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord("c"):
        capture = True

# release results to webcam
video_capture.release()
cv2.destroyAllWindows()