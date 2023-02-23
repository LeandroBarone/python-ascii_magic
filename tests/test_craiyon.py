from ascii_magic import AsciiArt

import pytest


def test_from_dalle():
    pytest.skip('This test takes over one minute, you must enable it manually')
    my_art = AsciiArt.from_craiyon('A hyperrealistic portrait of a cow with noble clothes, digital art', debug=True)
    my_art.to_html_file('output_craiyon.html', columns=200)
