import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load face cascade and mask detection model
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
mask_model = load_model("mask_detector_model.h5")  # replace with your model path

def face_mask(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    output = image.copy()

    for (x, y, w, h) in faces:
        face_img = image[y:y+h, x:x+w]
        face_resized = cv2.resize(face_img, (224, 224))  # match model input size
        face_normalized = face_resized / 255.0
        face_input = np.expand_dims(face_normalized, axis=0)

        pred = mask_model.predict(face_input)[0][0]  # adjust depending on your model
        if pred > 0.5:
            label = "Mask Detected"
            color = (0, 255, 0)  # green
        else:
            label = "No Mask Detected"
            color = (0, 0, 255)  # red

        cv2.rectangle(output, (x, y), (x + w, y + h), color, 2)
        cv2.putText(
            output,
            label,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2,
        )

    return output
