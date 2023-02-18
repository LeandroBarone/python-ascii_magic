from ascii_magic.asciimagic import AsciiMagic, AsciiArt

from PIL import Image

from typing import Optional


def quick_test():
    AsciiMagic.quick_test()


def from_image(path: str) -> AsciiArt:
    return AsciiMagic.from_image_file(path)


def from_pillow_image(img: Image.Image) -> AsciiArt:
    return AsciiMagic.from_image(img)


def from_url(url: str) -> AsciiArt:
    return AsciiMagic.from_url(url)


def from_clipboard() -> AsciiArt:
    return AsciiMagic.from_clipboard()


def from_dalle(prompt: str, api_key: Optional[str] = None, debug: bool = False) -> AsciiArt:
    return AsciiMagic.from_dalle(prompt, api_key, debug)
