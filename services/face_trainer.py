import cv2
import os
import numpy as np


class FaceTrainer:

    def __init__(self):

        self.dataset_path = "dataset"

        self.recognizer = (
            cv2.face.LBPHFaceRecognizer_create()
        )

    def train_model(self):

        faces = []
        labels = []

        label_map = {}

        current_label = 0

        for person_name in os.listdir(
            self.dataset_path
        ):

            person_folder = os.path.join(
                self.dataset_path,
                person_name
            )

            if not os.path.isdir(
                person_folder
            ):
                continue

            label_map[current_label] = (
                person_name
            )

            for image_name in os.listdir(
                person_folder
            ):

                image_path = os.path.join(
                    person_folder,
                    image_name
                )

                image = cv2.imread(
                    image_path,
                    cv2.IMREAD_GRAYSCALE
                )

                faces.append(image)

                labels.append(
                    current_label
                )

            current_label += 1

        self.recognizer.train(
            faces,
            np.array(labels)
        )

        self.recognizer.save(
            "trainer/trainer.yml"
        )

        print(
            "Training completed successfully!"
        )

        return label_map