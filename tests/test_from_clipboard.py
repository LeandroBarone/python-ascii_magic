from ascii_magic import AsciiArt


def test_from_clipboard():
    # This test requires an image in the clipboard
    my_art = AsciiArt.from_clipboard()
    my_art.to_terminal()
