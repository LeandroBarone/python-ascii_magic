from ascii_magic import AsciiArt

import PIL.ImageEnhance


def test_exposed_pil_image():
    my_art = AsciiArt.from_image('chicken_transparent.png')
    my_art.image = PIL.ImageEnhance.Brightness(my_art.image).enhance(0.2)
    my_art.to_terminal()
