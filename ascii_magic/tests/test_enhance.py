from ascii_magic import AsciiArt


def test_enhance():
    my_art = AsciiArt.from_image('lion.jpg')
    my_art.to_image_file('output_lion_normal.png', enhance_image=False, full_color=True)
    my_art.to_image_file('output_lion_enhance.png', enhance_image=True, full_color=True)
