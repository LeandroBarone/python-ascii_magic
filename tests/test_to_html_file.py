from ascii_magic import AsciiArt


def test_to_html_file():
    my_art = AsciiArt.from_image('kid.jpg')
    my_art.to_html_file('kid.html')


def test_to_html_file_terminal_mode():
    my_art = AsciiArt.from_image('kid.jpg')
    my_art.to_html_file('kid_terminal.html', full_color=False)


def test_to_html_file_monochrome_mode():
    my_art = AsciiArt.from_image('kid.jpg')
    my_art.to_html_file('kid_monochrome.html', monochrome=True)
