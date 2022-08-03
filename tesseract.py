import cv2
import numpy as np
from PIL import Image
import pytesseract

myconfig = r"--psm 11 --oem 3"

def ocr(image):
    response = pytesseract.image_to_string(image, config= myconfig)
    return response




# def grayscale(image):
#     return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# def remove_noise(image):
#     return cv2.medianBlur(image, 5)

# def thersholding(image):
#     return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1] 


def ocr_image(path):
    img = cv2.imread(path)
    # img = grayscale(img)
    # img = thersholding(img)
    # img = remove_noise(img)
    text = ocr(img)
    text_lo = text.lower()
    # print("text_lo:", text_lo)
    return text_lo