from ascii_magic import AsciiArt


def test_to_file():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_file('lion.txt')
