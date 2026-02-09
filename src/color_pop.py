import cv2
import numpy as np

def apply_color_tint(gray, color):
    """
    Apply a single RGB color tint to a grayscale image
    """
    colored = np.zeros((gray.shape[0], gray.shape[1], 3), dtype=np.uint8)
    colored[:, :, 0] = gray * (color[0] / 255)
    colored[:, :, 1] = gray * (color[1] / 255)
    colored[:, :, 2] = gray * (color[2] / 255)
    return colored.astype(np.uint8)

def color_pop(image):
    # Resize for consistency (optional but nice)
    image = cv2.resize(image, (500, 500))

    # Convert to grayscale + increase contrast
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # Warhol-style colors (BGR)
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

    # Create 2x2 grid
    top = np.hstack((panels[0], panels[1]))
    bottom = np.hstack((panels[2], panels[3]))
    output = np.vstack((top, bottom))

    return output