
from os import environ
from os.path import join
from uuid import uuid4

from PIL import Image
from pytesseract import image_to_string
from django.core.files import File


# Enviroment variable for loading Tesseract languages
environ['TESSDATA_PREFIX'] = '/home/delkys/tessdata'


def extract_text(filename):
    """
    Given the name of a file, loads it and extract the text in it using
    Tesseract OCR engine
    """
    image = Image.open(filename)
    config = ('-l spa --oem 1')
    text = image_to_string(image, config=config)
    return text


def generate_random_filename():
    """
    Generate random identifier of 10 characters
    """
    return str(uuid4()).replace('-', '')[:10]


def save_simple_image(uploaded_file):
    """
    It saves an uploaded image into file system with a random name
    """
    filename = generate_random_filename()
    filename = filename + '.' + uploaded_file.name.split('.')[1]
    filename = join(join('media', 'simple'), filename)

    with open(filename, 'wb') as file:
        newfile = File(file)
        newfile.write(uploaded_file.read())

    return filename
