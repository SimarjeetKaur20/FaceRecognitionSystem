import cv2
import os
import json
import numpy as np


_TRAINER_DIR = "trainer"
_MODEL_PATH = os.path.join(_TRAINER_DIR, "trainer.yml")
_LABEL_MAP_PATH = os.path.join(_TRAINER_DIR, "label_map.json")


class FaceTrainer:
    """
    Trains an LBPH face recognition model from the dataset folder
    and persists both the model (trainer.yml) and the label→name
    mapping (label_map.json) so recognition is deterministic.
    """

    def __init__(self):
        self.dataset_path = "dataset"
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        os.makedirs(_TRAINER_DIR, exist_ok=True)

    def train_model(self):
        """
        Reads all images in dataset/<person>/, trains the LBPH model,
        saves trainer.yml and label_map.json.

        Returns:
            label_map (dict[int, str]): mapping of numeric label → person name
        """
        faces = []
        labels = []
        label_map = {}
        current_label = 0

        # Sort to ensure consistent ordering across runs / platforms
        for person_name in sorted(os.listdir(self.dataset_path)):
            person_folder = os.path.join(self.dataset_path, person_name)

            if not os.path.isdir(person_folder):
                continue

            label_map[current_label] = person_name

            for image_name in os.listdir(person_folder):
                image_path = os.path.join(person_folder, image_name)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

                if image is None:
                    continue  # skip unreadable files

                faces.append(image)
                labels.append(current_label)

            current_label += 1

        if not faces:
            print("No training data found in dataset folder.")
            return {}

        self.recognizer.train(faces, np.array(labels))
        self.recognizer.save(_MODEL_PATH)

        # Persist the label map so the recognizer doesn't rely on os.listdir order
        # Keys must be strings for JSON serialisation; convert back to int on load
        with open(_LABEL_MAP_PATH, "w") as f:
            json.dump({str(k): v for k, v in label_map.items()}, f, indent=2)

        print(
            f"Training completed. {len(faces)} images, "
            f"{len(label_map)} people trained."
        )
        return label_map
