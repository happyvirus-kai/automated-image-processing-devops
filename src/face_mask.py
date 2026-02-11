import cv2
import numpy as np

# Detect faces using Haar Cascade.
# Then check the lower half of each face for skin color.
# If there is little skin detected, assume a mask is worn.

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def _lower_face_has_skin(face_roi):
    """Return the ratio of skin-colored pixels in the lower half of the face."""
    h, w = face_roi.shape[:2]
    if h == 0 or w == 0:
        return 0.0

    # Get lower half of the detected face
    lower = face_roi[h // 2 : h, 0:w]
    if lower.size == 0:
        return 0.0

    # Convert to HSV color space for skin detection
    hsv = cv2.cvtColor(lower, cv2.COLOR_BGR2HSV)

    # Approximate HSV range for skin color
    lower_skin = np.array([0, 10, 60], dtype=np.uint8)
    upper_skin = np.array([20, 150, 255], dtype=np.uint8)

    skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
    skin_pixels = cv2.countNonZero(skin_mask)
    total_pixels = skin_mask.shape[0] * skin_mask.shape[1]

    return float(skin_pixels) / float(total_pixels) if total_pixels > 0 else 0.0


def face_mask(image, debug=False):
    """
    Detect faces and determine if a facemask is worn.
    Draws a box and label around each detected face.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    output = image.copy()

    for (x, y, w, h) in faces:
        face = image[y : y + h, x : x + w]

        try:
            skin_ratio = _lower_face_has_skin(face)
        except Exception:
            skin_ratio = 1.0

        # If skin ratio is low, assume a mask is present
        mask_detected = skin_ratio < 0.45

        if mask_detected:
            label = "Facemask Detected"
            color = (0, 255, 0)  # Green box
            text_color = (255, 255, 255)
        else:
            label = "Facemask Not Detected"
            color = (0, 0, 255)  # Red box
            text_color = (255, 255, 255)

        # Draw face rectangle
        cv2.rectangle(output, (x, y), (x + w, y + h), color, 2)

        # Draw background for text label
        cv2.rectangle(output, (x, y - 28), (x + w, y), color, -1)

        # Put label text
        cv2.putText(output, label, (x + 6, y - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)

        if debug:
            # Show skin ratio value below the face (for testing)
            debug_text = f"skin_ratio={skin_ratio:.2f}"
            cv2.putText(output, debug_text, (x, y + h + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

    return output


if __name__ == "__main__":
    # Open webcam. Press 'q' to exit.
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        out = face_mask(frame)
        cv2.imshow("Face Mask Detector (naive)", out)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
