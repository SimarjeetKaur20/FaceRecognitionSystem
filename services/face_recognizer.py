import cv2
import os


class FaceRecognizer:

    def __init__(self):

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

        self.recognizer = (
            cv2.face.LBPHFaceRecognizer_create()
        )

        self.recognizer.read(
            "trainer/trainer.yml"
        )

        self.label_map = {}

        self.load_labels()

    def load_labels(self):

        current_label = 0

        for person_name in os.listdir(
            "dataset"
        ):

            person_folder = os.path.join(
                "dataset",
                person_name
            )

            if os.path.isdir(person_folder):

                self.label_map[current_label] = (
                    person_name
                )

                current_label += 1

    def recognize_faces(self):

        camera = cv2.VideoCapture(0)

        while True:

            success, frame = camera.read()

            if not success:
                break

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5
            )

            for (x, y, w, h) in faces:

                face = gray[
                    y:y+h,
                    x:x+w
                ]

                label, confidence = (
                    self.recognizer.predict(face)
                )

                if confidence < 80:

                    name = self.label_map.get(
                        label,
                        "Unknown"
                    )

                else:
                    name = "Unknown"

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x+w, y+h),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    name,
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2
                )

            cv2.imshow(
                "Face Recognition",
                frame
            )

            key = cv2.waitKey(1)

            if key == 27:
                break

        camera.release()
        cv2.destroyAllWindows()