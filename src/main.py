import os
import cv2
from color_pop import color_pop
from neon_glow import neon_glow
from rain_snow import rain_snow
from face_mask import face_mask_detection

INPUT_DIR = "input"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_images():
    for file in os.listdir(INPUT_DIR):
        if file.lower().endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(INPUT_DIR, file)
            image = cv2.imread(path)

            if image is None:
                continue

            cv2.imwrite(
                os.path.join(OUTPUT_DIR, f"colorpop_{file}"),
                color_pop(image)
            )

            cv2.imwrite(
                os.path.join(OUTPUT_DIR, f"neon_{file}"),
                neon_glow(image)
            )

            cv2.imwrite(
                os.path.join(OUTPUT_DIR, f"rain_{file}"),
                rain_snow(image, "rain")
            )

            cv2.imwrite(
                os.path.join(OUTPUT_DIR, f"snow_{file}"),
                rain_snow(image, "snow")
            )

            cv2.imwrite(
                os.path.join(OUTPUT_DIR, f"mask_{file}"),
                face_mask_detection(image)
            )

if _name_ == "_main_":
    process_images()