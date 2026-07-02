import cv2
import os
import json
from datetime import datetime

from database.database import Database


_MODEL_PATH = os.path.join("trainer", "trainer.yml")
_LABEL_MAP_PATH = os.path.join("trainer", "label_map.json")

# Confidence threshold — LBPH: lower value = better match
_CONFIDENCE_THRESHOLD = 80


class FaceRecognizer:
    """
    Real-time face recognition using the trained LBPH model.

    Automatically marks attendance in the database the first time
    a recognised person is seen each day (de-duplication is handled
    by the database's UNIQUE constraint on (user_id, date)).
    """

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.label_map: dict[int, str] = {}
        self.db = Database()

        self._load_model()

    def _load_model(self):
        if not os.path.exists(_MODEL_PATH):
            raise FileNotFoundError(
                f"Trained model not found at '{_MODEL_PATH}'. "
                "Please run the trainer first."
            )

        self.recognizer.read(_MODEL_PATH)

        if os.path.exists(_LABEL_MAP_PATH):
            with open(_LABEL_MAP_PATH, "r") as f:
                raw = json.load(f)
            # JSON keys are always strings; convert back to int
            self.label_map = {int(k): v for k, v in raw.items()}
        else:
            # Fallback: rebuild from dataset folder (sorted for consistency)
            print(
                "Warning: label_map.json not found. "
                "Rebuilding from dataset folder — re-train to fix this."
            )
            for idx, name in enumerate(sorted(os.listdir("dataset"))):
                if os.path.isdir(os.path.join("dataset", name)):
                    self.label_map[idx] = name

    def recognize_faces(self):
        """
        Opens the webcam, performs real-time face recognition, and
        marks attendance for each recognised person.
        Press ESC to quit.
        """
        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            print("Error: Cannot access webcam.")
            return

        # Track who has been notified/marked this session to avoid
        # flooding the terminal with repeated messages.
        marked_today: set[str] = set()

        print("Face recognition started. Press ESC to quit.")

        while True:
            success, frame = camera.read()
            if not success:
                print("Error reading frame.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.3, minNeighbors=5
            )

            for (x, y, w, h) in faces:
                face_roi = gray[y : y + h, x : x + w]
                label, confidence = self.recognizer.predict(face_roi)

                if confidence < _CONFIDENCE_THRESHOLD:
                    name = self.label_map.get(label, "Unknown")
                    color = (0, 255, 0)  # green — recognised
                    display_text = f"{name} ({confidence:.1f})"

                    if name not in marked_today:
                        now = datetime.now()
                        marked = self.db.mark_attendance(
                            name=name,
                            date=now.strftime("%d-%m-%Y"),
                            time_str=now.strftime("%H:%M:%S"),
                        )
                        if marked:
                            print(
                                f"[{now.strftime('%H:%M:%S')}] "
                                f"Attendance marked for: {name}"
                            )
                        marked_today.add(name)
                else:
                    name = "Unknown"
                    color = (0, 0, 255)  # red — unknown
                    display_text = "Unknown"

                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(
                    frame,
                    display_text,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    color,
                    2,
                )

            cv2.imshow("Face Recognition System", frame)

            if cv2.waitKey(1) == 27:  # ESC
                break

        camera.release()
        cv2.destroyAllWindows()
        self.db.close()
        print("Recognition session ended.")
