import cv2
import numpy as np
from PIL import Image
from rembg import remove

RAMP = np.array(list(" .:-=+*#%@"))


def process(img_path, cols=95):
    img = Image.open(img_path)

    # Remove background
    img = remove(img)
    img = np.array(img.convert("L"))

    # Resize
    h, w = img.shape
    rows = int(cols * (h / w) * 0.54)
    img = cv2.resize(img, (cols, rows))

    # CLAHE (contrast)
    clahe = cv2.createCLAHE(clipLimit=3.5)
    img = clahe.apply(img)

    # Gamma correction
    img = ((img / 255.0) ** 1.9) * 255
    img = img.astype(np.uint8)  # <-- add this line

    # Edge enhancement
    edges = cv2.Canny(img.astype(np.uint8), 50, 150)
    img = cv2.addWeighted(img, 0.85, edges, 0.15, 0)

    # Map to ASCII
    idx = (img / 255 * (len(RAMP) - 1)).astype(int)
    ascii_img = ["".join(RAMP[i]) for i in idx]

    return ascii_img


if __name__ == "__main__":
    ascii_img = process("assets/input.jpg")

    with open("assets/ascii.txt", "w") as f:
        for row in ascii_img:
            f.write(row + "\n")

    print("ASCII saved to assets/ascii.txt")
