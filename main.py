from services.face_capture import FaceCapture


def main():

    person_name = input(
        "Enter Person Name: "
    )

    capture = FaceCapture()

    capture.capture_faces(
        person_name
    )


if __name__ == "__main__":
    main()