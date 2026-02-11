import cv2
import numpy as np
import random

def rain_snow(image, mode="rain"):
    output = image.copy()
    h, w, _ = output.shape
    rain_layer = np.zeros_like(output, dtype=np.uint8)

    if mode == "rain":
        for _ in range(1200):
            x = random.randint(0, w - 1)
            y = random.randint(0, h - 1)
            length = random.randint(10, 20)

            cv2.line(
                rain_layer,
                (x, y),
                (x + random.randint(-2, 2), y + length),
                (200, 200, 200),
                1
            )

        rain_layer = cv2.GaussianBlur(rain_layer, (5, 5), 0)
        output = cv2.addWeighted(output, 0.85, rain_layer, 0.3, 0)

    elif mode == "snow":
        # Increased snow density
        for _ in range(2000):
            x = random.randint(0, w - 1)
            y = random.randint(0, h - 1)
            radius = random.randint(2, 4)  # Larger snow size

            cv2.circle(rain_layer, (x, y), radius, (255, 255, 255), -1)

        rain_layer = cv2.GaussianBlur(rain_layer, (5, 5), 0)

        # Stronger blending so snow is visible
        output = cv2.addWeighted(output, 0.8, rain_layer, 0.7, 0)

    return output
