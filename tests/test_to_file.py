import ascii_magic


def test_to_file():
    my_art = ascii_magic.from_image('lion.jpg')
    my_art.to_file('lion.txt')
