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


def from_dalle(
    prompt: str,
    api_key: Optional[str] = None,
    debug: bool = False,
) -> AsciiArt:
    return AsciiArt.from_dalle(prompt, api_key, debug=debug)


def from_stable_diffusion(
    prompt: str,
    api_key: str,
    engine: Optional[str] = None,
    steps: int = 30,
    debug: bool = False,
) -> AsciiArt:
    return AsciiArt.from_stable_diffusion(prompt, api_key, engine=engine, steps=steps, debug=debug)


def from_craiyon(
    prompt: str,
    debug: bool = False,
) -> AsciiArt:
    return AsciiArt.from_craiyon(prompt, debug=debug)
