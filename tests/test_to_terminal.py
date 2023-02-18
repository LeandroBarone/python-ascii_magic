from ascii_magic import AsciiArt, Back, Front


def test_blue_back():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_terminal(back=Back.BLUE)


def test_red_front():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_terminal(front=Front.RED)


def no_color():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_terminal(monochrome=True)
