from ascii_magic import AsciiArt

import pytest


def test_from_clipboard():
    # This test requires an image in the clipboard
    try:
        my_art = AsciiArt.from_clipboard()
    except OSError:
        pytest.skip('No image found in the clipboard')

    my_art.to_terminal()
