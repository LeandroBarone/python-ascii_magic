from ascii_magic.constants import PALETTE, CHARS_BY_DENSITY, DEFAULT_STYLES

import colorama
import webbrowser
import urllib.request
from PIL import Image

from typing import Optional
from enum import Enum


__VERSION__ = 2


class Modes(Enum):
    ASCII = 'ASCII'
    TERMINAL = 'TERMINAL'
    HTML = 'HTML'
    HTML_TERMINAL = 'HTML_TERMINAL'
    HTML_MONOCHROME = 'HTML_MONOCHROME'


class AsciiArt:
    def __init__(self, image: Image.Image):
        self._image = image

    def to_ascii(
        self,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: Optional[str] = None,
        monochrome: bool = False,
        back: Optional[colorama.ansi.AnsiBack] = None,
        front: Optional[colorama.ansi.AnsiFore] = None,
        debug: bool = False,
    ):
        art = self._img_to_art(
            columns=columns,
            width_ratio=width_ratio,
            char=char,
            monochrome=monochrome,
            back=back,
            front=front,
            debug=debug,
        )
        return art

    def to_terminal(
        self,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: Optional[str] = None,
        monochrome: bool = False,
        back: Optional[colorama.ansi.AnsiBack] = None,
        front: Optional[colorama.ansi.AnsiFore] = None,
        debug: bool = False,
    ):
        art = self._img_to_art(
            columns=columns,
            width_ratio=width_ratio,
            char=char,
            monochrome=monochrome,
            back=back,
            front=front,
            debug=debug,
        )
        AsciiMagic.print_to_terminal(art)
        return art

    def to_file(
        self,
        path: str,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: Optional[str] = None,
        monochrome: bool = False,
        back: Optional[colorama.ansi.AnsiBack] = None,
        front: Optional[colorama.ansi.AnsiFore] = None,
        debug: bool = False,
    ):
        art = self._img_to_art(
            columns=columns,
            width_ratio=width_ratio,
            char=char,
            monochrome=monochrome,
            back=back,
            front=front,
            debug=debug,
        )
        AsciiMagic.save_to_file(path, art)
        return art

    def to_html(
        self,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: Optional[str] = None,
        monochrome: bool = False,
        full_color: bool = True,
        debug: bool = False,
    ):
        art = self._img_to_art(
            mode=Modes.HTML,
            columns=columns,
            width_ratio=width_ratio,
            char=char,
            monochrome=monochrome,
            full_color=full_color,
            debug=debug,
        )
        return art

    def to_html_file(
        self,
        path: str,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: Optional[str] = None,
        monochrome: bool = False,
        full_color: bool = True,
        debug: bool = False,
        styles: str = DEFAULT_STYLES,
        additional_styles: str = '',
        auto_open: bool = False,
    ):
        art = self._img_to_art(
            mode=Modes.HTML,
            columns=columns,
            width_ratio=width_ratio,
            char=char,
            monochrome=monochrome,
            full_color=full_color,
            debug=debug,
        )
        AsciiMagic.save_to_html_file(
            path,
            art,
            styles=styles,
            additional_styles=additional_styles,
            auto_open=auto_open
        )
        return art

    def _img_to_art(
        self,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: Optional[str] = None,
        mode: Modes = Modes.TERMINAL,
        monochrome: bool = False,
        full_color: bool = True,
        back: Optional[colorama.ansi.AnsiBack] = None,
        front: Optional[colorama.ansi.AnsiFore] = None,
        debug: bool = False,
    ) -> str:
        if mode == Modes.TERMINAL:
            if monochrome:
                mode = Modes.ASCII

        if mode == Modes.HTML:
            if back or front:
                raise ValueError('Back or front colors not supported for HTML files')

            if monochrome:
                mode = Modes.HTML_MONOCHROME
            if not monochrome and not full_color:
                mode = Modes.HTML_TERMINAL

        if mode not in Modes:
            raise ValueError('Unknown output mode ' + str(mode))

        img_w, img_h = self._image.size
        scalar = img_w*width_ratio / columns
        img_w = int(img_w*width_ratio / scalar)
        img_h = int(img_h / scalar)
        rgb_img = self._image.resize((img_w, img_h))
        color_palette = self._image.getpalette()

        grayscale_img = rgb_img.convert("L")

        chars = [char] if char else CHARS_BY_DENSITY

        if debug:
            rgb_img.save('rgb.jpg')
            grayscale_img.save('grayscale.jpg')

        lines = []
        for h in range(img_h):
            line = ''

            for w in range(img_w):
                # get brightness value
                brightness = grayscale_img.getpixel((w, h)) / 255
                pixel = rgb_img.getpixel((w, h))
                # getpixel() may return an int, instead of tuple of ints, if the source img is a PNG with a transparency layer
                if isinstance(pixel, int):
                    pixel = (pixel, pixel, 255) if color_palette is None else tuple(color_palette[pixel*3:pixel*3 + 3])

                srgb = [(v/255.0)**2.2 for v in pixel]
                char = chars[int(brightness * (len(chars) - 1))]
                line += self._build_char(char, srgb, brightness, mode, front)

            if mode == Modes.TERMINAL and front:
                line = str(front) + line + colorama.Fore.RESET
            if mode == Modes.TERMINAL and back:
                line = str(back) + line + colorama.Back.RESET
            lines.append(line)

        if mode == Modes.TERMINAL:
            return '\n'.join(lines) + colorama.Fore.RESET
        elif mode == Modes.ASCII:
            return '\n'.join(lines)
        else:  # HTML modes
            return '<br />'.join(lines)

    def _convert_color(self, rgb: list, brightness: float) -> dict:
        min_distance = 2
        index = 0

        for i in range(len(PALETTE)):
            tmp = [v*brightness for v in PALETTE[i][0]]
            distance = self._l2_min(tmp, rgb)

            if distance < min_distance:
                index = i
                min_distance = distance

        return {
            'term': PALETTE[index][1],
            'hex-term': PALETTE[index][2],
            'hex': '#{:02x}{:02x}{:02x}'.format(*(int(c*200+55) for c in rgb)),
        }

    def _l2_min(self, v1: list, v2: list) -> float:
        return (v1[0]-v2[0])**2 + (v1[1]-v2[1])**2 + (v1[2]-v2[2])**2

    def _build_char(
        self,
        char: str,
        srgb: list,
        brightness: float,
        mode: Modes = Modes.TERMINAL,
        front: Optional[colorama.ansi.AnsiFore] = None,
    ) -> str:
        color = self._convert_color(srgb, brightness)

        if mode == Modes.TERMINAL:
            if front:
                return char  # Front color will be set per-line
            else:
                return color['term'] + char

        elif mode == Modes.ASCII:
            return char

        elif mode == Modes.HTML_TERMINAL:
            c = color['hex-term']
            return f'<span style="color: {c}">{char}</span>'

        elif mode == Modes.HTML:
            c = color['hex']
            return f'<span style="color: {c}">{char}</span>'

        elif mode == Modes.HTML_MONOCHROME:
            return f'<span style="color: white">{char}</span>'


class AsciiMagic:
    @classmethod
    def from_url(cls, url: str) -> AsciiArt:
        img = cls._load_url(url)
        return AsciiArt(img)

    @classmethod
    def from_image(cls, img: Image.Image) -> AsciiArt:
        return AsciiArt(img)

    @classmethod
    def from_image_file(cls, path: str) -> AsciiArt:
        img = cls._load_file(path)
        return AsciiArt(img)

    @classmethod
    def from_clipboard(cls) -> AsciiArt:
        img = cls._load_clipboard()
        return AsciiArt(img)

    @classmethod
    def quick_test(cls):
        img = cls.from_url('https://source.unsplash.com/800x600?landscapes')
        img.to_terminal()

    @classmethod
    def print_to_terminal(cls, art: str):
        colorama.init()
        print(art)

    @classmethod
    def save_to_html_file(
        cls,
        path: str,
        art: str,
        styles: str = DEFAULT_STYLES,
        additional_styles: str = '',
        auto_open: bool = False,
    ) -> None:
        html = f"""<!DOCTYPE html>
    <head>
        <title>ASCII art</title>
        <meta name="generator" content="ASCII Magic {__VERSION__} - https://github.com/LeandroBarone/python-ascii_magic/" />
    </head>
    <body>
        <pre style="{styles} {additional_styles}">{art}</pre>
    </body>
    </html>"""
        with open(path, 'w') as f:
            f.write(html)
        if auto_open:
            webbrowser.open(path)

    @classmethod
    def save_to_file(cls, path: str, art: str) -> None:
        with open(path, 'w') as f:
            f.write(art)

    @classmethod
    def _load_url(cls, url: str) -> Image.Image:
        with urllib.request.urlopen(url) as response:
            return Image.open(response)

    @classmethod
    def _load_file(cls, path: str) -> Image.Image:
        return Image.open(path)

    @classmethod
    def _load_clipboard(cls) -> Image.Image:
        try:
            from PIL import ImageGrab
            img = ImageGrab.grabclipboard()
        except (NotImplementedError, ImportError):
            img = cls._load_clipboard_linux()

        if not img:
            raise OSError('The clipboard does not contain an image')

        return img

    @classmethod
    def _load_clipboard_linux(cls) -> Image.Image:
        try:
            import gi  # type: ignore
            gi.require_version("Gtk", "3.0")  # type: ignore
            from gi.repository import Gtk, Gdk  # type: ignore
        except ModuleNotFoundError:
            print('Accessing the clipboard under Linux requires the PyGObject module')
            print('Ubuntu/Debian: sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0')
            print('Fedora: sudo dnf install python3-gobject gtk3')
            print('Arch: sudo pacman -S python-gobject gtk3')
            print('openSUSE: sudo zypper install python3-gobject python3-gobject-Gdk typelib-1_0-Gtk-3_0 libgtk-3-0')
            exit()

        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        try:
            buffer = clipboard.wait_for_image()
            data = buffer.get_pixels()
            w = buffer.props.width
            h = buffer.props.height
            stride = buffer.props.rowstride
        except Exception:
            raise OSError('The clipboard does not contain an image')

        mode = 'RGB'
        img = Image.frombytes(mode, (w, h), data, 'raw', mode, stride)
        return img
