from ascii_magic import AsciiArt


def test_to_html_file():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_html_file('lion.html')


def test_to_html_file_terminal_mode():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_html_file('lion_terminal.html', full_color=False)


def test_to_html_file_monochrome_mode():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_html_file('lion_monochrome.html', monochrome=True)
