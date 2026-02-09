import cv2
import numpy as np

def neon_glow(image):
    # Convert to gray for edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Stronger edges
    edges = cv2.Canny(gray, 80, 180)

    # Invert edges for glow base
    edges_inv = cv2.bitwise_not(edges)

    # Create neon color (cyan/purple tone)
    neon_color = np.zeros_like(image)
    neon_color[:, :, 0] = edges_inv   # Blue
    neon_color[:, :, 1] = edges_inv   # Green
    neon_color[:, :, 2] = edges_inv // 2  # Red (less)

    # Multi-layer blur = glow depth
    glow1 = cv2.GaussianBlur(neon_color, (9, 9), 0)
    glow2 = cv2.GaussianBlur(neon_color, (21, 21), 0)

    glow = cv2.addWeighted(glow1, 0.6, glow2, 0.4, 0)

    # Blend glow with original image
    output = cv2.addWeighted(image, 0.75, glow, 0.6, 0)

    return output