import cv2

def pencil_sketch(image_path, output_path):
    img = cv2.imread(image_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted_img = 255 - gray_img
    blurred_img = cv2.GaussianBlur(inverted_img, (21, 21), 0)
    sketch_img = cv2.divide(gray_img, 255 - blurred_img, scale=256)
    cv2.imwrite(output_path, sketch_img)

# Example usage
pencil_sketch("image.png", "pencil_sketch.png")
