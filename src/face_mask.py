import cv2
import numpy as np

# Optional: for future mask model
try:
    from tensorflow.keras.models import load_model
    model_available = True
except ImportError:
    model_available = False

# Load face cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Load mask model if available
mask_model = None
if model_available:
    try:
        mask_model = load_model("mask_detector_model.h5")
    except:
        mask_model = None  # model not found, fallback to demo mode
        print("Mask model not found, running in demo mode.")

def face_mask(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    output = image.copy()

    for (x, y, w, h) in faces:
        face_img = image[y:y+h, x:x+w]

        # Check if mask model is available
        if mask_model:
            # Preprocess for model (adjust depending on your model)
            face_resized = cv2.resize(face_img, (224, 224))
            face_normalized = face_resized / 255.0
            face_input = np.expand_dims(face_normalized, axis=0)

            pred = mask_model.predict(face_input)[0][0]  # adjust for your model
            if pred > 0.5:
                label = "Mask Detected"
                color = (0, 255, 0)
            else:
                label = "Face Mask Not Detected"
                color = (0, 0, 255)
        else:
            # Demo mode: always no mask
            label = "Face Mask Not Detected"
            color = (0, 0, 255)

        # Draw rectangle and label
        cv2.rectangle(output, (x, y), (x + w, y + h), color, 2)
        cv2.putText(
            output,
            label,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    return output
