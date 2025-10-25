from ascii_magic import AsciiArt

import pytest
import os


def test_from_swamui():
    if not os.environ.get('SWARMUI_SERVER'):
        pytest.skip('No SwarmUI server found on environment (KEY=SWARMUI_SERVER)')

    my_art = AsciiArt.from_swamui(
        'A hyperrealistic portrait of a cow with noble clothes, digital art',
        raw_input={
            'width': 1344,
            'height': 768,
        }
    )
    my_art.to_image_file('test_swarmui.png', full_color=True)
