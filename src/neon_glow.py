import cv2
import numpy as np

# Load image
img = cv2.imread("input_images/person.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Simple person segmentation (replace with proper segmentation for real use)
_, mask = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Detect edges of person
edges = cv2.Canny(mask, 50, 150)

# Create neon-colored outline
neon_color = np.array([0, 255, 255])  # Cyan
neon_img = np.zeros_like(img)
neon_img[edges != 0] = neon_color

# Add glow by blurring
glow = cv2.GaussianBlur(neon_img, (15, 15), 0)

# Overlay glow on black background
cv2.imwrite("output_images/person_neonglow.jpg", glow)