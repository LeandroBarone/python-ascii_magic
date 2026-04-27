__version__ = '2.7.5'

from ascii_magic.ascii_art_font import AsciiArtFont
from ascii_magic.color_data import ColorData
from ascii_magic.constants import (
    Front,
    Back,
    Modes,
    CHARS_BY_DENSITY,
    DEFAULT_STYLES,
    PALETTE,
    DEFAULT_GEMINI_MODEL,
    RESAMPLING_METHOD,
    PILLOW_VERSION,
)

from PIL import Image, ImageDraw, ImageEnhance

import io
import json
import os
import typing as t
import urllib.request
import urllib.parse
import warnings
import webbrowser
from time import time


class AsciiArt:
    __VERSION__ = __version__
    __PILLOW_VERSION__ = PILLOW_VERSION
    _image: Image.Image

    def __init__(self, image: Image.Image):
        self._image = image

    @property
    def image(self) -> Image.Image:
        return self._image

    @image.setter
    def image(self, value: Image.Image):
        self._image = value

    def to_ascii(
        self,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: "t.Optional[str]" = None,
        monochrome: bool = False,
        enhance_image: bool = False,
        back: "t.Optional[Back]" = None,
        front: "t.Optional[Front]" = None,
        debug: bool = False,
    ):
        art = self._img_to_art(
            columns=columns,
            width_ratio=width_ratio,
            char=char,
            mode=Modes.ASCII,
            monochrome=monochrome,
            enhance_image=enhance_image,
            back=back,
            front=front,
            debug=debug,
        )
        if isinstance(art, list):
            raise Exception('_img_to_art() returned a list in ASCII mode')
        return art

    def to_terminal(
        self,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: "t.Optional[str]" = None,
        enhance_image: bool = False,
        monochrome: bool = False,
        back: "t.Optional[Back]" = None,
        front: "t.Optional[Front]" = None,
        debug: bool = False,
    ):
        art = self._img_to_art(
            columns=columns,
            width_ratio=width_ratio,
            char=char,
            enhance_image=enhance_image,
            monochrome=monochrome,
            back=back,
            front=front,
            debug=debug,
        )
        if isinstance(art, list):
            raise Exception('_img_to_art() returned a list in TERMINAL mode')
        print(art)
        return art

    def to_file(
        self,
        path: str,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: "t.Optional[str]" = None,
        enhance_image: bool = False,
        monochrome: bool = False,
        back: "t.Optional[Back]" = None,
        front: "t.Optional[Front]" = None,
        debug: bool = False,
    ):
        art = self._img_to_art(
            columns=columns,
            width_ratio=width_ratio,
            char=char,
            enhance_image=enhance_image,
            monochrome=monochrome,
            back=back,
            front=front,
            debug=debug,
        )
        if isinstance(art, list):
            raise Exception('_img_to_art() returned a list in TERMINAL mode')
        self._save_string_to_text_file(path, art)
        return art

    def to_image_file(
        self,
        path: str,
        width: "t.Union[int, t.Literal['auto']]" = 'auto',
        height: "t.Union[int, t.Literal['auto']]" = 'auto',
        border_width: int = 2,
        stroke_width: float = 0.5,
        file_type: "t.Literal['PNG', 'JPG', 'GIF', 'WEBP']" = 'PNG',
        font: str = 'courier_prime.ttf',
        columns: int = 120,
        width_ratio: "t.Union[float, t.Literal['auto']]" = 'auto',
        char: "t.Optional[str]" = None,
        enhance_image: bool = False,
        monochrome: bool = False,
        full_color: bool = False,
        front: "t.Optional[t.Union[Front, str]]" = None,
        back: "t.Union[Back, str]" = '#000000',
        debug: bool = False,
    ):
        try:
            ascii_font = AsciiArtFont(font)
        except FileNotFoundError:
            raise FileNotFoundError(f'Font {font} not found')

        if width_ratio == 'auto':
            width_ratio = ascii_font.get_ratio()

        art = self._img_to_art(
            mode=Modes.OBJECT,
            columns=columns,
            width_ratio=width_ratio,
            char=char,
            enhance_image=enhance_image,
            monochrome=monochrome,
            full_color=full_color,
            back=back,
            front=front,
            debug=debug,
        )
        if isinstance(art, str):
            raise Exception('_img_to_art() returned a string in OBJECT mode')

        self._save_list_to_image_file(
            path,
            art,
            font=ascii_font,
            width=width,
            height=height,
            border_width=border_width,
            stroke_width=stroke_width if PILLOW_VERSION >= '9.0.0' else int(stroke_width),
            file_type=file_type,
            monochrome=monochrome,
            full_color=full_color,
            front=front,
            back=back,
        )
        return art

    def to_html(
        self,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: "t.Optional[str]" = None,
        enhance_image: bool = False,
        monochrome: bool = False,
        full_color: bool = False,
        debug: bool = False,
    ):
        art = self._img_to_art(
            mode=Modes.HTML,
            columns=columns,
            width_ratio=width_ratio,
            char=char,
            enhance_image=enhance_image,
            monochrome=monochrome,
            full_color=full_color,
            debug=debug,
        )
        if isinstance(art, list):
            raise Exception('_img_to_art() returned a list in HTML mode')
        return art

    def to_html_file(
        self,
        path: str,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: "t.Optional[str]" = None,
        enhance_image: bool = False,
        monochrome: bool = False,
        full_color: bool = True,
        styles: str = DEFAULT_STYLES,
        additional_styles: str = '',
        auto_open: bool = False,
        debug: bool = False,
    ):
        art = self._img_to_art(
            mode=Modes.HTML,
            columns=columns,
            width_ratio=width_ratio,
            char=char,
            enhance_image=enhance_image,
            monochrome=monochrome,
            full_color=full_color,
            debug=debug,
        )
        if isinstance(art, list):
            raise Exception('_img_to_art() returned a list in HTML mode')
        self._save_to_html_file(
            path,
            art,
            styles=styles,
            additional_styles=additional_styles,
            auto_open=auto_open
        )
        return art

    def to_character_list(
        self,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: "t.Optional[str]" = None,
        monochrome: bool = False,
        full_color: bool = False,
        back: "t.Optional[Back]" = None,
        front: "t.Optional[Front]" = None,
        debug: bool = False,
    ) -> "t.List[t.List[t.Dict[str, str]]]":
        art = self._img_to_art(
            mode=Modes.OBJECT,
            columns=columns,
            width_ratio=width_ratio,
            char=char,
            monochrome=monochrome,
            full_color=full_color,
            back=back,
            front=front,
            debug=debug,
        )
        if isinstance(art, str):
            raise Exception('_img_to_art() returned a string in OBJECT mode')
        return [
            [
                {
                    'character': art.character,
                    'terminal-color': art.terminal_color,
                    'terminal-hex-color': art.terminal_hex_color,
                    'full-hex-color': art.full_hex_color,
                }
                for art in line
            ]
            for line in art
        ]

    def _img_to_art(
        self,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: "t.Optional[str]" = None,
        mode: Modes = Modes.TERMINAL,
        enhance_image: bool = False,
        monochrome: bool = False,
        full_color: bool = False,
        front: "t.Optional[t.Union[Front, str]]" = None,
        back: "t.Optional[t.Union[Back, str]]" = None,
        debug: bool = False,
    ) -> "t.Union[str, t.List[t.List[ColorData]]]":
        if monochrome and full_color:
            full_color = False

        if mode == Modes.TERMINAL and monochrome:
            mode = Modes.ASCII

        if mode == Modes.HTML:
            if monochrome:
                mode = Modes.HTML_MONOCHROME
            elif full_color:
                mode = Modes.HTML_FULL_COLOR
            else:
                mode = Modes.HTML_TERMINAL

        if mode not in Modes:
            raise ValueError('Unknown output mode ' + str(mode))

        img_w, img_h = self._image.size
        scalar = img_w * width_ratio / columns
        img_w = int(img_w * width_ratio / scalar)
        img_h = int(img_h / scalar)
        rgb_img = self._image.resize((img_w, img_h))
        if enhance_image:
            rgb_img = ImageEnhance.Brightness(rgb_img).enhance(1.2)
            rgb_img = ImageEnhance.Color(rgb_img).enhance(1.2)
        color_palette = self._image.getpalette()

        grayscale_img = rgb_img.convert("L")

        chars = char if char else CHARS_BY_DENSITY

        if debug:
            rgb_img.save('rgb.jpg')
            grayscale_img.save('grayscale.jpg')

        lines: "t.List[t.List[ColorData]]" = []
        for h in range(img_h):
            line: "t.List[ColorData]" = []
            for w in range(img_w):
                # get brightness value
                brightness = self.get_brightness_value(grayscale_img, w, h)
                pixel = rgb_img.getpixel((w, h))

                # getpixel() may return an int, instead of tuple of ints, if the source img is a PNG with a transparency layer
                if isinstance(pixel, (int, float)):
                    pixel = (pixel, pixel, 255) if color_palette is None else tuple(color_palette[pixel * 3:pixel * 3 + 3])
                elif pixel is None:
                    pixel = (0, 0, 0)

                rgb = [(v / 255.0)**2.2 for v in pixel]
                char = chars[int(brightness * (len(chars) - 1))]
                character = self.get_color_data(char, rgb, brightness)

                line.append(character)
            lines.append(line)

        if mode == Modes.ASCII:
            art = ''
            for line in lines:
                for character in line:
                    art += character.character
                art += '\n'
            return art

        if mode == Modes.TERMINAL:
            art = ''
            for line in lines:
                if back:
                    art += self.get_charcode(back)

                previous_color = None
                for character in line:
                    current_color = self.get_charcode(front) if front else character.terminal_color
                    if current_color == previous_color:
                        art += character.character
                    else:
                        previous_color = current_color
                        art += current_color + character.character

                if back:
                    art += self.get_charcode(Back.RESET)

                art += self.get_charcode(Front.RESET)
                art += '\n'
            return art

        if mode == Modes.OBJECT:
            return [
                [c for c in line]
                for line in lines
            ]

        if mode == Modes.HTML_MONOCHROME:
            art = ''
            for line in lines:
                art += '<span>'

                for character in line:
                    art += '<span>' + character.character + '</span>'

                art += '</span>'
                art += '<br />'
            return art

        if mode == Modes.HTML_TERMINAL:
            art = ''
            for line in lines:
                art += '<span>'

                for character in line:
                    art += f'<span style="color:{character.terminal_hex_color}">' + character.character + '</span>'

                art += '</span>'
                art += '<br />'

            return art

        if mode == Modes.HTML_FULL_COLOR:
            art = ''
            for line in lines:
                art += '<span>'

                for character in line:
                    art += f'<span style="color:{character.full_hex_color}">' + character.character + '</span>'

                art += '</span>'
                art += '<br />'

            return art

    @staticmethod
    def get_brightness_value(img: Image.Image, w: int, h: int) -> float:
        pixel = img.getpixel((w, h))
        if isinstance(pixel, (float, int)):
            return pixel / 255
        elif isinstance(pixel, (list, tuple)) and len(pixel) > 0:
            return float(pixel[0]) / 255
        else:
            return 0

    @staticmethod
    def get_charcode(color: "t.Union[Front, Back, str]") -> str:
        if isinstance(color, str):
            return ''
        return '\033[' + str(color.value) + 'm'

    @staticmethod
    def cc(color: "t.Union[Front, Back, str]") -> str:
        # cc() is now an alias for get_charcode(), for backwards compatibility
        return AsciiArt.get_charcode(color)

    @staticmethod
    def color_to_hex(color: "t.Union[Front, Back, str]") -> str:
        if isinstance(color, (Front, Back)):
            if color.name == 'BLACK': return '#000000'
            if color.name == 'RED': return '#FF0000'
            if color.name == 'GREEN': return '#00FF00'
            if color.name == 'YELLOW': return '#FFFF00'
            if color.name == 'BLUE': return '#0000FF'
            if color.name == 'MAGENTA': return '#FF00FF'
            if color.name == 'CYAN': return '#00FFFF'
            if color.name == 'WHITE': return '#FFFFFF'
            if color.name == 'LIGHTBLACK': return '#222222'
            if color.name == 'LIGHTRED': return '#FF6666'
            if color.name == 'LIGHTGREEN': return '#66FF66'
            if color.name == 'LIGHTYELLOW': return '#FFFF66'
            if color.name == 'LIGHTBLUE': return '#6666FF'
            if color.name == 'LIGHTMAGENTA': return '#FF66FF'
            if color.name == 'LIGHTCYAN': return '#66FFFF'
            if color.name == 'LIGHTWHITE': return '#FFFFFF'
            raise ValueError('Unknown color ' + str(color))
        return color

    @staticmethod
    def l2_min(
        v1: "t.Union[t.List[float], t.Tuple[float, float, float]]",
        v2: "t.Union[t.List[float], t.Tuple[float, float, float]]"
    ) -> float:
        return (v1[0] - v2[0])**2 + (v1[1] - v2[1])**2 + (v1[2] - v2[2])**2

    @classmethod
    def get_color_data(
        cls,
        char: str,
        rgb: "t.Union[t.List[float], t.Tuple[float, float, float]]",
        brightness: float
    ) -> ColorData:
        min_distance = 2
        index = 0

        for i in range(len(PALETTE)):
            tmp = [v * brightness for v in PALETTE[i][0]]
            distance = cls.l2_min(tmp, rgb)

            if distance < min_distance:
                index = i
                min_distance = distance

        return ColorData(
            character=char,
            terminal_color=cls.get_charcode(PALETTE[index][1]),
            terminal_hex_color=PALETTE[index][2],
            full_hex_color='#{:02x}{:02x}{:02x}'.format(*(int(c * 200 + 55) for c in rgb)),
        )

    @staticmethod
    def _save_string_to_text_file(path: str, art: str) -> None:
        with open(path, 'w') as f:
            f.write(art)

    @classmethod
    def _save_list_to_image_file(
        cls,
        path: str,
        art: "t.List[t.List[ColorData]]",
        width: "t.Union[int, t.Literal['auto']]" = 'auto',
        height: "t.Union[int, t.Literal['auto']]" = 'auto',
        border_width: int = 2,
        stroke_width: float = 0.5,
        file_type: "t.Literal['PNG', 'JPG', 'GIF', 'WEBP']" = 'PNG',
        font: "t.Optional[AsciiArtFont]" = None,
        monochrome: bool = False,
        full_color: bool = False,
        front: "t.Optional[t.Union[Front, str]]" = None,
        back: "t.Optional[t.Union[Back, str]]" = None,
    ) -> None:
        if font is None:
            font = AsciiArtFont('courier_prime.ttf')
        char_width, _, line_height = font.get_char_size()

        if back is None:
            back = '#000000'
        if isinstance(back, Back):
            back = cls.color_to_hex(back)
        if isinstance(front, Front):
            front = cls.color_to_hex(front)

        cols = max(len(line) for line in art)
        rows = len(art)

        img_width = cols * char_width + border_width * 2
        img_height = rows * line_height + border_width * 2

        img = Image.new('RGB', (img_width, img_height), color=back)
        draw = ImageDraw.Draw(img)

        y = border_width + int(line_height / 2) + 1
        for line in art:
            x = border_width
            for character in line:
                fg_color = None
                if front:
                    fg_color = front
                elif full_color:
                    fg_color = character.full_hex_color
                elif monochrome:
                    fg_color = '#FFFFFF'
                else:
                    fg_color = character.terminal_hex_color

                draw.text(
                    (x, y),
                    character.character,
                    anchor='lm',
                    fill=fg_color,
                    font=font.get_font(),
                    stroke_width=stroke_width,
                )
                x += char_width
            y += line_height

        target_width = width if width != 'auto' else img_width
        target_height = height if height != 'auto' else img_height

        if target_width != img_width and height == 'auto':
            target_height = int(target_height * target_width / img_width)
        if target_height != img_height and width == 'auto':
            target_width = int(target_width * target_height / img_height)

        if target_width != img_width or target_height != img_height:
            img = img.resize((target_width, target_height), RESAMPLING_METHOD)

        # Pillow uses "JPEG" while the public API accepts the common alias "JPG".
        pil_format = 'JPEG' if file_type.upper() == 'JPG' else file_type
        img.save(path, pil_format)

    @staticmethod
    def _save_to_html_file(
        path: str,
        art: str,
        styles: str = DEFAULT_STYLES,
        additional_styles: str = '',
        auto_open: bool = False,
    ) -> None:
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>ASCII art</title>
    <meta name="generator" content="ASCII Magic {__version__} - https://github.com/LeandroBarone/python-ascii_magic/" />
</head>
<body>
    <pre style="{styles} {additional_styles}">{art}</pre>
</body>
</html>
        """
        with open(path, 'w') as f:
            f.write(html.strip())
        if auto_open:
            webbrowser.open(path)

    @classmethod
    def quick_test(cls):
        img = cls.from_url('https://cataas.com/cat')
        img.to_terminal()

    @classmethod
    def print_palette(cls):
        for f in Front:
            if f == Front.RESET:
                continue
            for b in Back:
                if b == Back.RESET:
                    continue
                print(
                    f.name + ' on ' + b.name + ' = ',
                    cls.get_charcode(f),
                    cls.get_charcode(b),
                    'ASCII_MAGIC',
                    cls.get_charcode(Front.RESET),
                    cls.get_charcode(Back.RESET),
                )

    @classmethod
    def from_url(cls, url: str) -> 'AsciiArt':
        img = cls._load_url(url)
        return AsciiArt(img)

    @classmethod
    def from_image(cls, path: str) -> 'AsciiArt':
        img = cls._load_file(path)
        return AsciiArt(img)

    @classmethod
    def from_pillow_image(cls, img: Image.Image) -> 'AsciiArt':
        return AsciiArt(img)

    @classmethod
    def from_clipboard(cls) -> 'AsciiArt':
        img = cls._load_clipboard()
        return AsciiArt(img)

    @classmethod
    def from_gemini(
        cls,
        prompt: str,
        model: str = DEFAULT_GEMINI_MODEL,
        api_key: "t.Optional[str]" = None,
        debug: bool = False
    ) -> 'AsciiArt':
        image = cls._load_gemini(prompt, model=model, api_key=api_key, debug=debug)
        return AsciiArt(image)

    @classmethod
    def from_swarmui(
        cls,
        prompt: str,
        width: int = 1280,
        height: int = 720,
        steps: int = 20,
        raw_input: "t.Dict[str, t.Any]" = {},
        server: str = 'http://localhost:7801',
        model: str = 'auto',
        debug: bool = False
    ) -> 'AsciiArt':
        image = cls._load_swarmui(
            prompt,
            width=width,
            height=height,
            steps=steps,
            raw_input=raw_input,
            server=server,
            model=model,
            debug=debug,
        )
        return AsciiArt(image)

    @staticmethod
    def _load_url(url: str) -> Image.Image:
        with urllib.request.urlopen(url) as response:
            return Image.open(response)

    @staticmethod
    def _load_file(path: str) -> Image.Image:
        return Image.open(path)

    @classmethod
    def _load_clipboard(cls) -> Image.Image:
        try:
            from PIL import ImageGrab
            result = ImageGrab.grabclipboard()
        except (NotImplementedError, ImportError):
            warnings.warn("""
Pillow cannot access the clipboard on this operating system.
Recent Pillow versions can attempt to use wl-paste or xclip on Linux.
Attempting to use PyGObject...
            """.strip())
            result = cls._load_clipboard_pygobject()

        if result is None or (isinstance(result, list) and len(result) == 0):
            raise OSError('The clipboard does not contain an image')

        if isinstance(result, Image.Image):
            # win32 or gtk single image
            return result
        else:
            # win32 file list
            return Image.open(result[0])

    @staticmethod
    def _load_clipboard_pygobject() -> Image.Image:
        try:
            import gi  # type: ignore[reportMissingImports]
            gi.require_version("Gtk", "3.0")
            from gi.repository import Gtk, Gdk  # type: ignore[reportMissingImports]
        except ModuleNotFoundError:
            raise ModuleNotFoundError("PyGObject is not installed")

        try:
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            buffer = clipboard.wait_for_image()
            if not buffer:
                raise
            data = buffer.get_pixels()
            if not data:
                raise
        except Exception:
            raise OSError('The clipboard does not contain an image')

        w = buffer.props.width
        h = buffer.props.height
        stride = buffer.props.rowstride
        mode = 'RGB'
        img = Image.frombytes(mode, (w, h), data, 'raw', mode, stride)
        return img

    @staticmethod
    def _load_gemini(
        prompt: str,
        model: str = DEFAULT_GEMINI_MODEL,
        api_key: "t.Optional[str]" = None,
        debug: bool = False
    ) -> Image.Image:
        try:
            from google import genai
        except ModuleNotFoundError:
            print('Using Gemini requires the google-genai module')
            print('pip install google-genai')
            exit()

        environ_api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key and environ_api_key:
            api_key = environ_api_key

        if not api_key:
            raise ValueError('You must set up an API key before accessing Gemini')

        client = genai.Client(
            api_key=api_key,
        )

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )

        if not response or not response.parts:
            raise OSError('No images generated')

        if debug:
            with open(str(int(time())) + '_gemini.txt', 'w') as f:
                f.write(str(response))

        for part in response.parts:
            if part.inline_data:
                generated_image = part.as_image()
                if not generated_image or not generated_image.image_bytes:
                    continue
                if debug:
                    try:
                        with open(str(int(time())) + '_gemini.png', 'wb') as f:
                            f.write(generated_image.image_bytes)
                    except Exception:
                        pass
                return Image.open(io.BytesIO(generated_image.image_bytes))

        raise OSError('No images generated')

    @classmethod
    def _load_swarmui(
        cls,
        prompt: str,
        width: int = 1280,
        height: int = 720,
        steps: int = 20,
        raw_input: "t.Dict[str, t.Any]" = {},
        server: str = 'http://localhost:7801',
        model: str = 'auto',
        debug: bool = False
    ) -> Image.Image:
        environ_server = os.environ.get('SWARMUI_SERVER')
        if not server and environ_server:
            server = environ_server

        if not server:
            raise ValueError('You must set up a SwarmUI server before accessing SwarmUI')

        session_response = urllib.request.urlopen(
            urllib.request.Request(
                f'{server}/API/GetNewSession',
                data=json.dumps({}).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
        )
        session_data = json.loads(session_response.read().decode('utf-8'))
        session_id = session_data.get('session_id')

        if not session_id:
            raise OSError('Failed to obtain session_id from SwarmUI server')

        # Pick model from server if none was provided
        if model == 'auto':
            models_response = urllib.request.urlopen(
                urllib.request.Request(
                    f'{server}/API/ListModels',
                    data=json.dumps({
                        'session_id': session_id,
                        'path': '',
                        'depth': 3,
                    }).encode('utf-8'),
                    headers={'Content-Type': 'application/json'},
                    method='POST',
                )
            )

            models = json.loads(models_response.read().decode('utf-8'))

            if debug:
                with open(str(int(time())) + '_swarmui_ListModels_response.txt', 'w') as f:
                    f.write(str(models))

            model = models['files'][0]['name']

        generate_response = urllib.request.urlopen(
            urllib.request.Request(
                f'{server}/API/GenerateText2Image',
                data=json.dumps({
                    'session_id': session_id,
                    'images': 1,
                    'model': model,
                    'prompt': prompt,
                    'width': width,
                    'height': height,
                    'steps': steps,
                    **raw_input,
                }).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST',
            )
        )

        generate_data = json.loads(generate_response.read().decode('utf-8'))

        if debug:
            with open(str(int(time())) + '_swarmui_GenerateText2Image_response.txt', 'w') as f:
                f.write(str(generate_data))

        if 'error' in generate_data:
            raise OSError(generate_data['error'])

        if 'images' in generate_data and len(generate_data['images']) > 0:
            image_path = generate_data['images'][0]
            image_path_parsed = urllib.parse.quote(image_path, safe='/')
            image_url = f'{server}/{image_path_parsed}'
            return cls._load_url(image_url)

        raise OSError('No images generated by SwarmUI')
