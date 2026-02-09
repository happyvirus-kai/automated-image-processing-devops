import os
import cv2
from color_pop import color_pop
from neon_glow import neon_glow
from rain_snow import rain_snow
from face_mask import face_mask

INPUT_DIR = "input"
OUTPUT_DIR = "output"

# make sure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

for file in os.listdir(INPUT_DIR):
    if file.lower().endswith((".png", ".jpg", ".jpeg")):
        print("Processing:", file)  # <-- debug print
        img_path = os.path.join(INPUT_DIR, file)
        img = cv2.imread(img_path)

        pop_img = color_pop(img)
        neon_img = neon_glow(img)
        rain_img = rain_snow(img)
        mask_img = face_mask(img)

        cv2.imwrite(os.path.join(OUTPUT_DIR, "pop_" + file), pop_img)
        cv2.imwrite(os.path.join(OUTPUT_DIR, "neon_" + file), neon_img)
        cv2.imwrite(os.path.join(OUTPUT_DIR, "rain_" + file), rain_img)
        cv2.imwrite(os.path.join(OUTPUT_DIR, "mask_" + file), mask_img)

print("Processing complete!")
