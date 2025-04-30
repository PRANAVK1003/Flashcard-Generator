import cv2
import pytesseract
import numpy as np
from PIL import Image

def preprocess_image(image_path):
    """ Load & preprocess the image for OCR with enhanced techniques """
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Error: Unable to load image {image_path}")
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian Blur before thresholding
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Adaptive thresholding for better results
        processed = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        return processed

    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def extract_text(image_path):
    """ Extract text with OCR """
    processed_img = preprocess_image(image_path)
    if processed_img is None:
        return ""

    # Run OCR with optimized settings
    text = pytesseract.image_to_string(processed_img, config="--psm 6 --oem 3")

    return text.strip()
