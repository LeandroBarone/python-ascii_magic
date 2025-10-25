from ascii_magic import AsciiArt

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


def from_gemini(
    prompt: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    debug: bool = False,
) -> AsciiArt:
    return AsciiArt.from_gemini(prompt, api_key, model, debug)
