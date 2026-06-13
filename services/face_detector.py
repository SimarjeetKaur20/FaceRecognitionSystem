import cv2

class FaceDetector:

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

    def start_detection(self):

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            print("Error: Cannot access webcam")
            return

        while True:

            success, frame = camera.read()

            if not success:
                print("Error reading frame")
                break

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5,
                minSize=(30, 30)
            )

            for (x, y, w, h) in faces:

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

            cv2.imshow(
                "Face Recognition System - Face Detection",
                frame
            )

            key = cv2.waitKey(1)

            if key == 27:  # ESC key
                break

        camera.release()
        cv2.destroyAllWindows()