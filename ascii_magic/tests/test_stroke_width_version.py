from PIL import Image
import PIL.ImageDraw

import ascii_magic.ascii_art as ascii_art_mod
from ascii_magic import AsciiArt


def test_pillow_major_version_parsing():
    assert ascii_art_mod._pillow_major_version('9.5.0') == 9
    assert ascii_art_mod._pillow_major_version('10.0.0') == 10
    assert ascii_art_mod._pillow_major_version('13.0.0') == 13
    assert ascii_art_mod._pillow_major_version('10.0.0rc1') == 10


def test_to_image_file_keeps_float_stroke_width_on_modern_pillow(tmp_path, monkeypatch):
    seen = {}
    real_draw = PIL.ImageDraw.Draw

    def spy_draw(image):
        draw = real_draw(image)
        original_text = draw.text

        def text(xy, content, **kwargs):
            seen.update(kwargs)
            return original_text(xy, content, **kwargs)

        draw.text = text
        return draw

    monkeypatch.setattr(PIL.ImageDraw, 'Draw', spy_draw)
    art = AsciiArt.from_pillow_image(Image.new('RGB', (32, 32), 'white'))
    art.to_image_file(str(tmp_path / 'stroke.png'), columns=8, stroke_width=0.5)
    assert seen.get('stroke_width') == 0.5
