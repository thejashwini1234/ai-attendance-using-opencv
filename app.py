import os
import csv
import time
import cv2
import face_recognition

# Paths
PHOTOS_DIR = 'student_photos'
ATTENDANCE_FILE = 'attendance.csv'

# Load student photos and get their encodings
print("Loading student photos...")
student_encodings = []
student_names = []
for filename in os.listdir(PHOTOS_DIR):
    image = face_recognition.load_image_file(os.path.join(PHOTOS_DIR, filename))
    encoding = face_recognition.face_encodings(image)[0]
    student_encodings.append(encoding)
    student_names.append(os.path.splitext(filename)[0])

# Load previous attendance records
attendance_records = {}
if os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            attendance_records[row['name']] = row
        print(f"Loaded {len(attendance_records)} previous attendance records.")

# Attendance tracking
last_attendance_time = {}

# Open webcam
print("Starting attendance monitoring...")
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Find all the faces in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop through the face encodings
    for face_encoding, face_location in zip(face_encodings, face_locations):
        # See if the face is a match for the known student photos
        matches = face_recognition.compare_faces(student_encodings, face_encoding)
        name = "No Name"

        # If a match was found, use the first one
        if True in matches:
            first_match_index = matches.index(True)
            name = student_names[first_match_index]

        # Check if the student has been marked already in the last hour
        current_time = time.time()
        if name not in attendance_records or current_time - last_attendance_time.get(name, 0) > 3600:
            # Record attendance
            attendance_record = {
                'name': name,
                'date': time.strftime('%Y-%m-%d'),
                'time': time.strftime('%H:%M:%S')
            }
            attendance_records[name] = attendance_record
            last_attendance_time[name] = current_time
            print(f"Attendance recorded for {name}")

    # Save attendance records to CSV
    with open(ATTENDANCE_FILE, 'w', newline='') as csvfile:
        fieldnames = ['name', 'date', 'time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for record in attendance_records.values():
            writer.writerow(record)

    # Display the camera feed
    for face_location in face_locations:
        # Extract the region of the image that contains the face
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with the name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        name_to_display = attendance_records.get(name, "No Name")
        cv2.putText(frame, str(name_to_display), (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    cv2.imshow('Attendance Monitor', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()