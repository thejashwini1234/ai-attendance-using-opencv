An AI-powered attendance system is a smart and efficient solution for automating attendance tracking in classrooms, workplaces, or events. This system leverages computer vision technology to recognize individuals through facial recognition and seamlessly records attendance at regular intervals.
In this implementation, OpenCV, a popular computer vision library, is utilized to process and analyze facial data. The system captures photos of individuals from a directory (student_photos) where each photo is labeled with the respective student’s name. These photos serve as the database for facial recognition. Once the system identifies a student, it records their attendance in a CSV file named attendance.csv.

Key features of this attendance system include:

Automated Attendance Recording: The system captures attendance hourly without human intervention. This ensures accuracy and eliminates errors associated with manual record-keeping.

Facial Recognition: By using OpenCV's advanced face detection and recognition capabilities, the system identifies individuals based on their facial features.

Data Storage: Attendance data is stored in a structured CSV file (attendance.csv) that includes details such as the student's name, time of attendance, and date. This provides an easily accessible and portable format for record-keeping and analysis.

User-Friendly Setup: The system is designed to work with a directory (student_photos) containing labeled images of students, making it easy to set up and expand as new students are added.

Scalability: The system can handle large numbers of students, making it suitable for schools, colleges, and corporate environments.

installation
1. opencv library
2. facerecognition library

After downloading

create a csv file with name attendance.csv

create a folder with name student_photos

store all the photos inside this folder only the photos inside this folder will be identified.
