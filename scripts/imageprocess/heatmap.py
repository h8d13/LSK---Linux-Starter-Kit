import cv2


def heatmap_effect(image_path, output_path):
    img = cv2.imread(image_path, 0)  # Load grayscale
    heatmap = cv2.applyColorMap(img, cv2.COLORMAP_JET)
    cv2.imwrite(output_path, heatmap)

# Example usage
heatmap_effect("image.png", "heatmap.png")
