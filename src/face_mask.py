import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Load mask classifier
mask_model = load_model("mask_detector_model.h5")

def face_mask(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    output = image.copy()

    for (x, y, w, h) in faces:
        face = image[y:y+h, x:x+w]

        # Preprocess
        face = cv2.resize(face, (224, 224))
        face = face.astype("float32") / 255.0
        face = np.expand_dims(face, axis=0)

        # Predict
        pred = mask_model.predict(face)[0]

        mask_prob = pred[0]
        no_mask_prob = pred[1]

        if mask_prob > no_mask_prob:
            label = "Face Mask Detected"
            color = (0, 255, 0)
        else:
            label = "No Face Mask Detected"
            color = (0, 0, 255)

        cv2.rectangle(output, (x, y), (x+w, y+h), color, 2)
        cv2.putText(output, label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    return output
