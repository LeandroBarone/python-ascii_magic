from ascii_magic import AsciiArt


def test_from_file():
    my_art = AsciiArt.from_image('kid.jpg')
    my_art.to_terminal()


def test_from_file_transparent_bg():
    my_art = AsciiArt.from_image('chicken_transparent.png')
    my_art.to_terminal()
