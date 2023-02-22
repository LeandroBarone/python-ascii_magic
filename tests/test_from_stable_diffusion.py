from ascii_magic import AsciiArt

import pytest

import os


def test_from_dalle():
    api_key = os.environ.get('MY_STABLE_DIFFUSION_API_KEY')

    if not api_key:
        pytest.skip('No Stable Diffusion API key found on environment (KEY=MY_STABLE_DIFFUSION_API_KEY)')

    my_art = AsciiArt.from_stable_diffusion('A hyperrealistic portrait of a cow with noble clothes, digital art', api_key, debug=True)
    my_art.to_html_file('output_stable_diffusion.html', columns=200)
