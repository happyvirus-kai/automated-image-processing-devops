import cv2
import numpy as np

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def detect_face_mask(image):
    output = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    for (x, y, w, h) in faces:
        face_roi = image[y:y+h, x:x+w]

        # Lower half of face (mask area)
        lower_face = face_roi[h//2:h, 🙂

        # Convert to HSV
        hsv = cv2.cvtColor(lower_face, cv2.COLOR_BGR2HSV)

        # Skin color range (approx)
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)

        skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)

        # Percentage of skin detected
        skin_ratio = np.sum(skin_mask > 0) / skin_mask.size

        # Decision rule
        if skin_ratio < 0.15:
            label = "MASK"
            color = (0, 255, 0)
        else:
            label = "NO MASK"
            color = (0, 0, 255)

        # Draw bounding box & label
        cv2.rectangle(output, (x, y), (x+w, y+h), color, 2)
        cv2.putText(
            output,
            label,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            color,
            2
        )

    return output