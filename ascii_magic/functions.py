from ascii_magic._ascii_magic import AsciiArt

from PIL import Image

from typing import Optional


def quick_test():
    AsciiArt.quick_test()


def from_image(path: str) -> AsciiArt:
    return AsciiArt.from_image(path)


def from_pillow_image(img: Image.Image) -> AsciiArt:
    return AsciiArt.from_pillow_image(img)


def from_url(url: str) -> AsciiArt:
    return AsciiArt.from_url(url)


def from_clipboard() -> AsciiArt:
    return AsciiArt.from_clipboard()


def from_dalle(prompt: str, api_key: Optional[str] = None, **kwargs) -> AsciiArt:
    return AsciiArt.from_dalle(prompt, api_key, **kwargs)
