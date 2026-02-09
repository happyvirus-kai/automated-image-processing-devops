import cv2
import numpy as np

def neon_glow(image, intensity=1.0):
    """Apply a vibrant, full-image neon cyberpunk grade.

    - Increases contrast and saturation
    - Maps luminance to a neon palette (purple/cyan/pink/yellow)
    - Adds bloom/glow and preserves subject details
    """
    # Resize for consistent output
    image = cv2.resize(image, (600, 800))

    # 1) Contrast enhancement using CLAHE on L channel
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge((l, a, b))
    contrast = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # 2) Increase saturation
    hsv = cv2.cvtColor(contrast, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.6, 0, 255)
    sat = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    # 3) Compute normalized luminance (0..1)
    lum = cv2.cvtColor(sat, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0

    # 4) Create neon palette mapping by interpolating between stops
    xs = np.array([0.0, 0.33, 0.66, 1.0])
    # palette in BGR (bright neon tones)
    B_vals = np.array([128, 255, 255, 0], dtype=np.float32)
    G_vals = np.array([0, 255, 0, 255], dtype=np.float32)
    R_vals = np.array([128, 0, 255, 255], dtype=np.float32)

    flat = lum.flatten()
    B = np.interp(flat, xs, B_vals).reshape(lum.shape)
    G = np.interp(flat, xs, G_vals).reshape(lum.shape)
    R = np.interp(flat, xs, R_vals).reshape(lum.shape)

    overlay = np.stack((B, G, R), axis=2).astype(np.uint8)

    # 5) Blend overlay with saturated image (screen-like blend)
    sat_f = sat.astype(np.float32)
    overlay_f = overlay.astype(np.float32)
    base = cv2.addWeighted(sat_f, 0.55, overlay_f, 0.8, 0)

    # 6) Add bloom/glow by blurring bright parts of overlay
    bright_mask = (lum > 0.5).astype(np.float32)
    bright = (overlay_f * bright_mask[:, :, None])
    glow1 = cv2.GaussianBlur(bright, (31, 31), 0)
    glow2 = cv2.GaussianBlur(bright, (61, 61), 0)
    glow = cv2.addWeighted(glow1, 0.8, glow2, 0.6, 0)

    # composite glow over base
    composed = cv2.addWeighted(base, 1.0, glow, 0.7 * intensity, 0)

    # 7) Preserve details: mild sharpening (unsharp mask)
    blurred = cv2.GaussianBlur(composed, (0, 0), sigmaX=3)
    sharp = cv2.addWeighted(composed, 1.4, blurred, -0.4, 0)

    # 8) Final tone+contrast tweak
    final = np.clip(sharp, 0, 255).astype(np.uint8)

    return final
    output = image.copy()
    mask3 = (person_mask_f > 0.5).astype(np.uint8)
    output = np.where(mask3 == 1, blended_region, output)

    return output