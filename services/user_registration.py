from services.face_capture import FaceCapture
from database.database import Database
from datetime import datetime

class UserRegistration:
    def __init__(self):
        self.face_capture = FaceCapture()
        self.database = Database()

    def register_user(self):
        person_name = input("Enter User Name: ").strip().title()
        if person_name == "":
            print("Name cannot be empty.")
            return
        if self.database.user_exists(person_name):
            print("User already exists.")
            self.database.close()
            return
        registration_date = datetime.now().strftime("%d-%m-%Y")
        print("\nOpening camera...\n")
        self.face_capture.capture_faces(person_name)
        self.database.add_user(
            person_name,
            registration_date
        )
        self.database.close()
        print("\nRegistration completed successfully!")