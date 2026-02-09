import cv2
import random  # for random mask assignment

# Load the Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def face_mask(image):
    # Convert the image to grayscale for detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    # Copy the image to draw on
    output = image.copy()

    # Loop over detected faces
    for (x, y, w, h) in faces:
        # Randomly decide if the face has a mask (50% chance)
        has_mask = random.choice([True, False])
        
        if has_mask:
            label = "Mask Detected"
            color = (0, 255, 0)  # green for mask
        else:
            label = "No Mask Detected"
            color = (0, 0, 255)  # red for no mask
        
        # Draw rectangle around the face
        cv2.rectangle(output, (x, y), (x + w, y + h), color, 2)
        
        # Put the text
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
