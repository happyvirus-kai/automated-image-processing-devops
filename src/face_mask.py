import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os

# Load face cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Load mask model safely
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "mask_detector_model.h5")

mask_model = None
if os.path.exists(MODEL_PATH):
    mask_model = load_model(MODEL_PATH)
else:
    print("Mask model not found — running without mask detection.")

def face_mask(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    output = image.copy()

    for (x, y, w, h) in faces:
        face_roi = image[y:y+h, x:x+w]

        if mask_model is not None:
            # Resize for model
            face = cv2.resize(face_roi, (224, 224))
            face = face.astype("float32") / 255.0
            face = np.expand_dims(face, axis=0)

            pred = mask_model.predict(face)[0]

            if pred[0] > pred[1]:
                label = "Face Mask Detected"
                color = (0, 255, 0)
            else:
                label = "No Face Mask Detected"
                color = (0, 0, 255)

        else:
            label = "Model Not Loaded"
            color = (0, 0, 255)

        cv2.rectangle(output, (x, y), (x+w, y+h), color, 2)
        cv2.putText(
            output,
            label,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

    return output
