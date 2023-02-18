import ascii_magic
from PIL import Image


def test_from_pillow_image():
    with Image.open('moon.jpg') as img:
        my_art = ascii_magic.from_pillow_image(img)
        my_art.to_terminal()
