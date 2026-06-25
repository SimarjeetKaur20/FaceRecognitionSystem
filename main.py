# for capturing faces
"""
from services.face_capture import FaceCapture
def main():
    person_name = input("Enter Person Name: ")
    capture = FaceCapture()
    capture.capture_faces(person_name)
if __name__ == "__main__":
    main()
"""
# for training model
"""
from services.face_trainer import FaceTrainer
def main():
    trainer = FaceTrainer()
    trainer.train_model()
if __name__ == "__main__":
    main()
"""
# for recognizing faces
"""
from services.face_recognizer import FaceRecognizer
def main():
    recognizer = FaceRecognizer()
    recognizer.recognize_faces()
if __name__ == "__main__":
    main()
"""
# for database addition
"""
from database.database import Database
from datetime import datetime
def main():
    db = Database()
    name = input("Enter Name: ").strip()
    today = datetime.now().strftime("%d-%m-%Y")
    db.add_user(name, today)
    print("\nRegistered Users")
    print("----------------")
    users = db.get_all_users()
    for user in users:
        print(user)
    db.close()
if __name__ == "__main__":
    main()
"""
# for particular database deletion
"""
from database.database import Database
def main():
    db = Database()
    db.delete_user("mmy")
    print("\nRemaining Users:\n")
    users = db.get_all_users()
    for user in users:
        print(user)
    db.close()
if __name__ == "__main__":
    main()
"""
# for temporary database deletion
"""
from database.database import Database
db = Database()
db.reset_users_table()
db.close()
"""
# for user registration

from services.user_registration import UserRegistration
def main():
    registration = UserRegistration()
    registration.register_user()
if __name__ == "__main__":
    main()