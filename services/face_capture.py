import cv2
import os


class FaceCapture:

    def __init__(self):

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

    def capture_faces(self, person_name):

        dataset_path = os.path.join(
            "dataset",
            person_name
        )

        os.makedirs(
            dataset_path,
            exist_ok=True
        )

        camera = cv2.VideoCapture(0)

        count = 0

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

                count += 1

                image_path = os.path.join(
                    dataset_path,
                    f"{count}.jpg"
                )

                cv2.imwrite(
                    image_path,
                    face
                )

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x+w, y+h),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Images Captured: {count}/50",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

            cv2.imshow(
                "Register User",
                frame
            )

            if cv2.waitKey(1) == 27:
                break

            if count >= 50:
                break

        camera.release()
        cv2.destroyAllWindows()

        print(
            f"{count} images saved for {person_name}"
        )