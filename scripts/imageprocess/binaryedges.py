import cv2
import numpy as np

def generate_binary_edges(image_path, output_path=None):
    # Load the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Step 1: Enhance contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_img = clahe.apply(img)
    
    # Step 2: Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(enhanced_img, (5, 5), 0)
    
    # Step 3: Use Sobel edge detection
    sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)  # Horizontal edges
    sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)  # Vertical edges
    sobel = cv2.magnitude(sobelx, sobely)  # Magnitude of gradients
    sobel = np.uint8(np.clip(sobel, 0, 255))  # Convert to 8-bit

    # Step 4: Normalize Sobel and apply binary threshold
    normalized_sobel = cv2.normalize(sobel, None, 0, 255, cv2.NORM_MINMAX)
    _, binary_edges = cv2.threshold(normalized_sobel, 50, 255, cv2.THRESH_BINARY)

    # Step 5: Save the binary edge image if an output path is specified
    if output_path:
        cv2.imwrite(output_path, binary_edges)

    return binary_edges

if __name__ == "__main__":
    # Example usage
    image_path = "image.png"  # Input image path
    output_path = "binary_edges.png"  # Output binary edge image path
    
    binary_edges = generate_binary_edges(image_path, output_path=output_path)
    print("Binary edges have been generated and saved.")
