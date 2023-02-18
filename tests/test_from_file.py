import ascii_magic


def test_from_file():
    my_art = ascii_magic.from_image_file('kid.jpg')
    my_art.to_terminal()


def test_from_file_transparent_bg():
    my_art = ascii_magic.from_image_file('chicken_transparent.png')
    my_art.to_terminal()
