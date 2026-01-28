from ascii_magic import AsciiArt
from ascii_magic.constants import DEFAULT_GEMINI_MODEL

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
    model: str = DEFAULT_GEMINI_MODEL,
    debug: bool = False,
) -> AsciiArt:
    return AsciiArt.from_gemini(prompt, model, api_key, debug)


def from_swarmui(
    prompt: str,
    width: int = 1280,
    height: int = 720,
    steps: int = 20,
    raw_input: dict = {},
    server: str = 'http://localhost:7801',
    model: str = 'auto',
    debug: bool = False,
) -> AsciiArt:
    return AsciiArt.from_swarmui(prompt, width, height, steps, raw_input, server, model, debug)
