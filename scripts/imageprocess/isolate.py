import cv2
import numpy as np

def isolate_color(image_path, output_path, color='red'):
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Define color range
    if color == 'red':
        lower = np.array([0, 50, 50])
        upper = np.array([10, 255, 255])
    elif color == 'blue':
        lower = np.array([100, 50, 50])
        upper = np.array([140, 255, 255])
    elif color == 'green':
        lower = np.array([40, 50, 50])
        upper = np.array([80, 255, 255])
    
    mask = cv2.inRange(hsv, lower, upper)
    color_img = cv2.bitwise_and(img, img, mask=mask)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    combined_img = np.where(mask[:, :, None].astype(bool), color_img, gray_img)
    
    cv2.imwrite(output_path, combined_img)

# Example usage
isolate_color("image.png", "red_highlight.png", color='red')
