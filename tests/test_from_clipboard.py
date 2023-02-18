import ascii_magic


def test_from_clipboard():
    # This test requires an image in the clipboard
    my_art = ascii_magic.from_clipboard()
    my_art.to_terminal()
