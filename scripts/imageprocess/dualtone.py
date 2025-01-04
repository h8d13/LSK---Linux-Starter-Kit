import cv2
from PIL import Image
import numpy as np

def dual_tone(image_path, output_path, color1=(0, 128, 255), color2=(255, 128, 0)):
    from PIL import ImageOps

    img = Image.open(image_path).convert("L")  # Convert to grayscale
    gradient = np.linspace(0, 1, 256)  # Create gradient
    gradient_map = np.array([
        (int(color1[0] * (1 - val) + color2[0] * val),
         int(color1[1] * (1 - val) + color2[1] * val),
         int(color1[2] * (1 - val) + color2[2] * val))
        for val in gradient
    ])
    img = ImageOps.autocontrast(img)
    img_data = np.asarray(img)
    img_colored = gradient_map[img_data]
    Image.fromarray(np.uint8(img_colored)).save(output_path)

# Example usage
dual_tone("image.png", "dual_tone.png", color1=(0, 0, 255), color2=(255, 255, 0))
