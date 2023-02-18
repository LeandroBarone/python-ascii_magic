import ascii_magic


def test_to_html_file():
    my_art = ascii_magic.from_image('kid.jpg')
    my_art.to_html_file('kid.html')


def test_to_html_file_terminal_mode():
    my_art = ascii_magic.from_image('kid.jpg')
    my_art.to_html_file('kid_terminal.html', full_color=False)


def test_to_html_file_monochrome_mode():
    my_art = ascii_magic.from_image('kid.jpg')
    my_art.to_html_file('kid_monochrome.html', monochrome=True)
