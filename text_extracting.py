import cv2
from PIL import Image
import pytesseract
import argparse
import os
import json


def to_text(path):  # Извлечение текста из файла (задание № 1)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    text = pytesseract.image_to_string(Image.open(filename), lang='eng+rus')
    os.remove(filename)
    return str({'text': ' '.join(' '.join(text.split("\n")).split())})
