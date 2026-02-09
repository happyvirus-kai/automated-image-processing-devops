import cv2
import numpy as np

def neon_effect(image):
    """Apply neon glow effect around the person's outline."""
    # Resize for consistency
    image = cv2.resize(image, (600, 800))

    # Convert to HSV for better skin detection
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Detect skin/person using HSV range (simple segmentation)
    # Lower and upper bounds for skin color in HSV
    lower_skin = np.array([0, 10, 60], dtype=np.uint8)
    upper_skin = np.array([20, 150, 255], dtype=np.uint8)
    
    skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    # Improve mask with morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)
    
    # Dilate to connect nearby regions
    skin_mask = cv2.dilate(skin_mask, kernel, iterations=3)
    
    # Find edges of the person
    edges = cv2.Canny(skin_mask, 50, 150)
    
    # Thicken edges for better visibility
    thick_kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, thick_kernel, iterations=2)
    
    # Create neon color (bright cyan/electric blue)
    neon = np.zeros_like(image)
    neon[:, :, 0] = edges * 255   # Blue channel
    neon[:, :, 1] = edges * 255   # Green channel
    neon[:, :, 2] = edges * 100   # Red channel (less red for cyan)
    
    neon = np.clip(neon, 0, 255).astype(np.uint8)
    
    # Create multiple glow layers for bloom effect
    glow1 = cv2.GaussianBlur(neon, (11, 11), 0)
    glow2 = cv2.GaussianBlur(neon, (21, 21), 0)
    glow3 = cv2.GaussianBlur(neon, (41, 41), 0)
    
    # Combine glow layers
    glow = cv2.addWeighted(glow1, 0.8, glow2, 0.5, 0)
    glow = cv2.addWeighted(glow, 1.0, glow3, 0.3, 0)
    
    # Darken background slightly
    dark_bg = cv2.addWeighted(image, 0.4, np.zeros_like(image), 0, 0)
    
    # Combine dark background with neon glow
    output = cv2.addWeighted(dark_bg, 1.0, glow, 1.5, 0)
    output = cv2.addWeighted(output, 1.0, neon, 2.0, 0)
    
    return output