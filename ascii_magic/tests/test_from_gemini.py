from ascii_magic import AsciiArt

import pytest

import os


def test_from_gemini():
    if not os.environ.get('GEMINI_API_KEY'):
        pytest.skip('No Gemini API key found on environment (KEY=GEMINI_API_KEY)')

    my_art = AsciiArt.from_gemini('A hyperrealistic portrait of a cow with noble clothes, digital art')
    my_art.to_terminal()
