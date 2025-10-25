from ascii_magic import AsciiArt


def test_to_image_file_monochrome():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_image_file(
        'output_lion_monochrome.png',
        columns=60,
        monochrome=True,
    )


def test_to_image_file_green():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_image_file(
        'output_lion_green.png',
        columns=60,
        front='#00FF00',
        back='#222',
    )


def test_to_image_file_console():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_image_file(
        'output_lion_console.png',
        columns=60,
    )


def test_to_image_file_full_color():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_image_file(
        'output_lion_full_color.png',
        columns=60,
        full_color=True,
        height='auto',
    )


def test_to_image_file_small_width():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_image_file(
        'output_lion_small_width.png',
        columns=60,
        width=200,
    )


def test_to_image_file_small_height():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_image_file(
        'output_lion_small_height.png',
        columns=60,
        height=200,
    )


def test_to_image_file_square():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_image_file(
        'output_lion_square.png',
        columns=60,
        width=200,
        height=200,
    )
