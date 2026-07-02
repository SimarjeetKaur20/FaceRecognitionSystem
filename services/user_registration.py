import os
import shutil
from datetime import datetime

from services.face_capture import FaceCapture
from database.database import Database


class UserRegistration:
    """Handles new user registration: DB entry + face dataset capture."""

    def __init__(self):
        self.face_capture = FaceCapture()
        self.database = Database()

    def register_user(self):
        person_name = input("Enter User Name: ").strip().title()

        if not person_name:
            print("Name cannot be empty.")
            return

        if self.database.user_exists(person_name):
            print(f"User '{person_name}' already exists.")
            self.database.close()
            return

        registration_date = datetime.now().strftime("%d-%m-%Y")

        print(f"\nRegistering '{person_name}'...")
        print("Opening camera — look at the camera and wait for capture.\n")

        self.face_capture.capture_faces(person_name)

        # Assign label_id = next available integer (used by trainer/recognizer)
        existing_users = self.database.get_all_users()
        next_label = len(existing_users)  # 0-based index

        self.database.add_user(person_name, registration_date, label_id=next_label)
        print(f"\nRegistration completed for '{person_name}' (label_id={next_label}).")
        print("Remember to re-train the model to include this new user.")

        self.database.close()

    def delete_user(self, person_name: str):
        """
        Remove a user from the database AND delete their dataset folder.
        Does NOT automatically re-train — caller should do that if needed.
        """
        person_name = person_name.strip().title()

        if not self.database.user_exists(person_name):
            print(f"User '{person_name}' not found.")
            self.database.close()
            return

        # Remove from DB (cascades attendance via FK)
        self.database.delete_user(person_name)

        # Remove dataset folder
        dataset_folder = os.path.join("dataset", person_name)
        if os.path.isdir(dataset_folder):
            shutil.rmtree(dataset_folder)
            print(f"Dataset folder '{dataset_folder}' deleted.")
        else:
            print(f"No dataset folder found for '{person_name}'.")

        print(f"User '{person_name}' fully removed. Re-train the model to apply changes.")
        self.database.close()
