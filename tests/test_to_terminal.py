import ascii_magic


def test_blue_back():
    my_art = ascii_magic.from_image_file('lion.jpg')
    my_art.to_terminal(back=ascii_magic.Back.BLUE)


def test_red_front():
    my_art = ascii_magic.from_image_file('lion.jpg')
    my_art.to_terminal(front=ascii_magic.Front.RED)


def no_color():
    my_art = ascii_magic.from_image_file('lion.jpg')
    my_art.to_terminal(monochrome=True)
