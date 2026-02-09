import cv2
import numpy as np

def neon_glow(image):
    """Apply realistic neon outline effect with multi-colored glow.
    
    Detects outlines of face, hair, eyes, and background details,
    then highlights them with bright neon colors (cyan, magenta, yellow, green)
    on a dark background with soft glow effect.
    """
    # Resize for consistency
    image = cv2.resize(image, (600, 800))
    h, w = image.shape[:2]

    # Create dark background (mostly black with slight original image)
    dark_bg = cv2.addWeighted(image, 0.15, np.zeros_like(image), 0, 0)
    
    # Convert to grayscale for general edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Detect edges using Canny
    edges = cv2.Canny(blurred, 30, 100)
    
    # Dilate edges for thicker, more visible lines
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    edges = cv2.dilate(edges, kernel, iterations=2)
    
    # Detect skin/face using HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 10, 60], dtype=np.uint8)
    upper_skin = np.array([20, 150, 255], dtype=np.uint8)
    skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
    skin_mask = cv2.dilate(skin_mask, kernel, iterations=2)
    
    # Find face edges
    face_edges = cv2.Canny(skin_mask, 50, 150)
    face_edges = cv2.dilate(face_edges, kernel, iterations=2)
    
    # Combine all edges
    combined_edges = cv2.bitwise_or(edges, face_edges)
    
    # Create multi-colored neon effect
    neon = np.zeros_like(image)
    
    # Apply different neon colors to different regions
    # Cyan for general edges
    neon_cyan = np.zeros_like(image)
    neon_cyan[:, :, 0] = combined_edges * 255  # Blue
    neon_cyan[:, :, 1] = combined_edges * 255  # Green
    neon_cyan[:, :, 2] = combined_edges * 50   # Red
    
    # Magenta for face/skin edges
    neon_magenta = np.zeros_like(image)
    neon_magenta[:, :, 0] = face_edges * 200   # Blue
    neon_magenta[:, :, 1] = face_edges * 0     # Green
    neon_magenta[:, :, 2] = face_edges * 255   # Red
    
    # Yellow for additional highlights
    edges_inv = cv2.bitwise_not(combined_edges)
    neon_yellow = np.zeros_like(image)
    neon_yellow[:, :, 0] = combined_edges * 0      # Blue
    neon_yellow[:, :, 1] = combined_edges * 255    # Green
    neon_yellow[:, :, 2] = combined_edges * 255    # Red
    
    # Combine all neon colors
    neon = cv2.addWeighted(neon_cyan, 0.6, neon_magenta, 0.4, 0)
    neon = cv2.addWeighted(neon, 1.0, neon_yellow, 0.2, 0)
    neon = np.clip(neon, 0, 255).astype(np.uint8)
    
    # Create multiple soft glow layers for realistic neon lighting
    glow1 = cv2.GaussianBlur(neon, (15, 15), 0)
    glow2 = cv2.GaussianBlur(neon, (25, 25), 0)
    glow3 = cv2.GaussianBlur(neon, (51, 51), 0)
    
    # Combine glow layers with different intensities
    glow = cv2.addWeighted(glow1, 1.0, glow2, 0.6, 0)
    glow = cv2.addWeighted(glow, 1.0, glow3, 0.3, 0)
    
    # Blend dark background with glow and neon edges
    output = dark_bg.copy()
    output = cv2.addWeighted(output, 1.0, glow, 1.2, 0)
    output = cv2.addWeighted(output, 1.0, neon, 2.0, 0)
    
    return output