from ascii_magic import AsciiArt

import pytest

import os


def test_from_dalle():
    api_key = os.environ.get('MY_DALLE_API_KEY')

    if not api_key:
        pytest.skip('No DALL-E API key found on environment (KEY=MY_DALLE_API_KEY)')

    my_art = AsciiArt.from_dalle('A hyperrealistic portrait of a cow with noble clothes, digital art', api_key, debug=True)
    my_art.to_html_file('output_dalle.html', columns=200)
