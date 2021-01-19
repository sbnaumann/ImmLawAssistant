try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import argparse

def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

# print(ocr_core('images/ocr_example_1.png'))


def ArgChecker():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs='?')
    args = parser.parse_args()
    if args.filename is None:
        parser.error("This python program requires a full filepath to run")
    else:
        print(ocr_core(args.filename))


if __name__ == '__main__':
    ArgChecker()
