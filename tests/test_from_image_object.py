from ascii_magic import AsciiArt
from PIL import Image


def test_from_pillow_image():
    with Image.open('moon.jpg') as img:
        my_art = AsciiArt.from_pillow_image(img)
        my_art.to_terminal()
