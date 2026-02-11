import cv2
import numpy as np

def neon_glow(image, intensity=1.0):
    """
    Apply a neon cyberpunk effect to the entire image.

    - Boosts contrast and saturation
    - Maps brightness to neon colors
    - Adds glow/bloom effect
    - Sharpens details
    """

    # Resize image for consistent output size
    image = cv2.resize(image, (600, 800))

    # Enhance contrast using CLAHE on the lightness channel
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge((l, a, b))
    contrast = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # Increase color saturation
    hsv = cv2.cvtColor(contrast, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.6, 0, 255)
    sat = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    # Compute normalized brightness (0 to 1)
    lum = cv2.cvtColor(sat, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0

    # Define neon color palette (BGR values)
    xs = np.array([0.0, 0.33, 0.66, 1.0])
    B_vals = np.array([128, 255, 255, 0], dtype=np.float32)
    G_vals = np.array([0, 255, 0, 255], dtype=np.float32)
    R_vals = np.array([128, 0, 255, 255], dtype=np.float32)

    # Map brightness to neon colors
    flat = lum.flatten()
    B = np.interp(flat, xs, B_vals).reshape(lum.shape)
    G = np.interp(flat, xs, G_vals).reshape(lum.shape)
    R = np.interp(flat, xs, R_vals).reshape(lum.shape)

    overlay = np.stack((B, G, R), axis=2).astype(np.uint8)

    # Blend neon overlay with saturated image
    sat_f = sat.astype(np.float32)
    overlay_f = overlay.astype(np.float32)
    base = cv2.addWeighted(sat_f, 0.55, overlay_f, 0.8, 0)

    # Create glow effect from bright areas
    bright_mask = (lum > 0.5).astype(np.float32)
    bright = (overlay_f * bright_mask[:, :, None])
    glow1 = cv2.GaussianBlur(bright, (31, 31), 0)
    glow2 = cv2.GaussianBlur(bright, (61, 61), 0)
    glow = cv2.addWeighted(glow1, 0.8, glow2, 0.6, 0)

    # Add glow to image
    composed = cv2.addWeighted(base, 1.0, glow, 0.7 * intensity, 0)

    # Sharpen image slightly (unsharp mask)
    blurred = cv2.GaussianBlur(composed, (0, 0), sigmaX=3)
    sharp = cv2.addWeighted(composed, 1.4, blurred, -0.4, 0)

    # Final clipping to valid image range
    final = np.clip(sharp, 0, 255).astype(np.uint8)

    return final

    output = image.copy()
    mask3 = (person_mask_f > 0.5).astype(np.uint8)
    output = np.where(mask3 == 1, blended_region, output)

    return output
