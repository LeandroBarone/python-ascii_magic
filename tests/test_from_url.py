import ascii_magic


def test_from_url():
    my_art = ascii_magic.from_url('https://source.unsplash.com/800x600?nature')
    my_art.to_terminal()


def test_wrong_url():
    try:
        my_art = ascii_magic.from_url('https://images2.alphacoders.com/902/thumb-1920-902946.png')
        my_art.to_terminal()
    except OSError as e:
        print(f'Could not load the image, server said: {e.code} {e.msg}')  # type: ignore
