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

from services.face_recognizer import FaceRecognizer
def main():
    recognizer = FaceRecognizer()
    recognizer.recognize_faces()
if __name__ == "__main__":
    main()
