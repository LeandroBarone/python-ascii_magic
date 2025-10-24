from ascii_magic import AsciiArt


def test_chars_by_density():
    my_art = AsciiArt.from_image('kid.jpg')
    my_art.to_terminal(char=' .$@', columns=150)
