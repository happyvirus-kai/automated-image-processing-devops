import cv2

def neon_glow(image):
    edges = cv2.Canny(image, 100, 200)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    glow = cv2.GaussianBlur(edges_colored, (7, 7), 0)

    neon = cv2.addWeighted(image, 0.8, glow, 0.5, 0)
    return neon