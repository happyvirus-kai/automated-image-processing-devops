import cv2
import numpy as np
import random

def rain_snow(image, mode="rain"):
    output = image.copy()
    h, w, _ = output.shape

    if mode == "rain":
        for _ in range(800):
            x = random.randint(0, w - 1)
            y = random.randint(0, h - 1)
            cv2.line(output, (x, y), (x + 2, y + 10), (200, 200, 200), 1)

    elif mode == "snow":
        for _ in range(500):
            x = random.randint(0, w - 1)
            y = random.randint(0, h - 1)
            cv2.circle(output, (x, y), 1, (255, 255, 255), -1)

    return output