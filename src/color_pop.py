import cv2
import numpy as np

def apply_color_tint(gray, color):
    """
    Apply an RGB color tint to a grayscale image.
    """
    # Create an empty 3-channel image (for BGR color)
    colored = np.zeros((gray.shape[0], gray.shape[1], 3), dtype=np.uint8)

    # Apply the color tint by scaling each channel
    colored[:, :, 0] = gray * (color[0] / 255)
    colored[:, :, 1] = gray * (color[1] / 255)
    colored[:, :, 2] = gray * (color[2] / 255)

    return colored.astype(np.uint8)

def color_pop(image):
    # Resize image to 500x500 for uniform output size
    image = cv2.resize(image, (500, 500))

    # Convert image to grayscale and enhance contrast
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # Define four BGR colors for the pop-art effect
    colors = [
        (0, 255, 0),     # Green
        (255, 255, 0),   # Cyan
        (0, 255, 255),   # Yellow
        (255, 0, 255)    # Pink
    ]

    panels = []
    for color in colors:
        panel = apply_color_tint(gray, color)
        panels.append(panel)

    # Combine images into a 2x2 grid
    top = np.hstack((panels[0], panels[1]))
    bottom = np.hstack((panels[2], panels[3]))
    output = np.vstack((top, bottom))

    return output
