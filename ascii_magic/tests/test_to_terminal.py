from ascii_magic import AsciiArt, Back, Front


def test_blue_back():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_terminal(columns=100, back=Back.BLUE)


def test_red_front():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_terminal(columns=100, front=Front.RED)


def test_monochrome():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_terminal(columns=100, monochrome=True)


def test_small():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_terminal(columns=50)
