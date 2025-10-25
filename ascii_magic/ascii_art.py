from ascii_magic.constants import Front, Back, Modes, CHARS_BY_DENSITY, DEFAULT_STYLES, PALETTE
from ascii_magic.ascii_art_font import AsciiArtFont

from PIL import Image, ImageDraw, ImageEnhance

import io
import os
import json
import webbrowser
import urllib.request
from typing import Optional, Union, Literal
from time import time


class AsciiArt:
    __VERSION__ = 2.7

    def __init__(self, image: Image.Image):
        self._image = image

    @property
    def image(self) -> Image.Image:
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    def to_ascii(
        self,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: Optional[str] = None,
        monochrome: bool = False,
        enhance_image: bool = False,
        back: Optional[Back] = None,
        front: Optional[Front] = None,
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
        return art

    def to_terminal(
        self,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: Optional[str] = None,
        enhance_image: bool = False,
        monochrome: bool = False,
        back: Optional[Back] = None,
        front: Optional[Front] = None,
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
        print(art)
        return art

    def to_file(
        self,
        path: str,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: Optional[str] = None,
        enhance_image: bool = False,
        monochrome: bool = False,
        back: Optional[Back] = None,
        front: Optional[Front] = None,
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
        self._save_to_file(path, art)
        return art

    def to_image_file(
        self,
        path: str,
        width: Union[int, Literal['auto']] = 'auto',
        height: Union[int, Literal['auto']] = 'auto',
        border_width: int = 2,
        stroke_width: float = 0.5,
        file_type: Literal['PNG', 'JPG', 'GIF', 'WEBP'] = 'PNG',
        font: str = 'courier_prime.ttf',
        columns: int = 120,
        width_ratio: Union[float, Literal['auto']] = 'auto',
        char: Optional[str] = None,
        enhance_image: bool = False,
        monochrome: bool = False,
        full_color: bool = False,
        front: Optional[Union[Front, str]] = None,
        back: str = '#000000',
        debug: bool = False,
    ):
        try:
            font = AsciiArtFont(font)
        except FileNotFoundError:
            raise FileNotFoundError(f'Font {font} not found')

        if width_ratio == 'auto':
            width_ratio = font.get_ratio()

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

        self._save_to_image_file(
            path,
            art,
            font=font,
            width=width,
            height=height,
            border_width=border_width,
            stroke_width=stroke_width,
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
        char: Optional[str] = None,
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
        return art

    def to_html_file(
        self,
        path: str,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: Optional[str] = None,
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
        char: Optional[str] = None,
        monochrome: bool = False,
        full_color: bool = False,
        back: Optional[Back] = None,
        front: Optional[Front] = None,
        debug: bool = False,
    ) -> list[list[dict]]:
        return self._img_to_art(
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

    def _img_to_art(
        self,
        columns: int = 120,
        width_ratio: float = 2.2,
        char: Optional[str] = None,
        mode: Modes = Modes.TERMINAL,
        enhance_image: bool = False,
        monochrome: bool = False,
        full_color: bool = False,
        back: Optional[Back] = None,
        front: Optional[Front] = None,
        debug: bool = False,
    ) -> str:
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

        lines = []
        for h in range(img_h):
            line = []
            for w in range(img_w):
                # get brightness value
                brightness = grayscale_img.getpixel((w, h)) / 255
                pixel = rgb_img.getpixel((w, h))

                # getpixel() may return an int, instead of tuple of ints, if the source img is a PNG with a transparency layer
                if isinstance(pixel, int):
                    pixel = (pixel, pixel, 255) if color_palette is None else tuple(color_palette[pixel * 3:pixel * 3 + 3])

                rgb = [(v / 255.0)**2.2 for v in pixel]
                char = chars[int(brightness * (len(chars) - 1))]
                character = self.get_color_data(char, rgb, brightness)

                line.append(character)
            lines.append(line)

        if mode == Modes.ASCII:
            art = ''
            for line in lines:
                for character in line:
                    art += character['character']
                art += '\n'
            return art

        if mode == Modes.TERMINAL:
            art = ''
            for line in lines:
                if back:
                    art += self.cc(back)

                previous_color = None
                for character in line:
                    current_color = self.cc(front) if front else character['terminal-color']
                    if current_color == previous_color:
                        art += character['character']
                    else:
                        previous_color = current_color
                        art += current_color + character['character']

                if back:
                    art += self.cc(Back.RESET)

                art += self.cc(Front.RESET)
                art += '\n'
            return art

        if mode == Modes.OBJECT:
            art = []
            for line in lines:
                art.append([])
                for character in line:
                    art[-1].append(character)
            return art

        if mode == Modes.HTML_MONOCHROME:
            art = ''
            for line in lines:
                art += '<span>'

                for character in line:
                    art += '<span>' + character['character'] + '</span>'

                art += '</span>'
                art += '<br />'
            return art

        if mode == Modes.HTML_TERMINAL:
            art = ''
            for line in lines:
                art += '<span>'

                for character in line:
                    art += f'<span style="color:{character["terminal-hex-color"]}">' + character['character'] + '</span>'

                art += '</span>'
                art += '<br />'

            return art

        if mode == Modes.HTML_FULL_COLOR:
            art = ''
            for line in lines:
                art += '<span>'

                for character in line:
                    art += f'<span style="color:{character["full-hex-color"]}">' + character['character'] + '</span>'

                art += '</span>'
                art += '<br />'

            return art

    @staticmethod
    def cc(color: Front | Back) -> str:
        return '\033[' + str(color.value) + 'm'

    @staticmethod
    def l2_min(v1: list, v2: list) -> float:
        return (v1[0] - v2[0])**2 + (v1[1] - v2[1])**2 + (v1[2] - v2[2])**2

    @staticmethod
    def get_color_data(char: str, rgb: Union[list, tuple], brightness: float) -> dict:
        min_distance = 2
        index = 0

        for i in range(len(PALETTE)):
            tmp = [v * brightness for v in PALETTE[i][0]]
            distance = AsciiArt.l2_min(tmp, rgb)

            if distance < min_distance:
                index = i
                min_distance = distance

        return {
            'character': char,
            'terminal-color': AsciiArt.cc(PALETTE[index][1]),
            'terminal-hex-color': PALETTE[index][2],
            'full-hex-color': '#{:02x}{:02x}{:02x}'.format(*(int(c * 200 + 55) for c in rgb)),
        }

    @staticmethod
    def _save_to_file(path: str, art: str) -> None:
        with open(path, 'w') as f:
            f.write(art)

    @staticmethod
    def _save_to_image_file(
        path: str,
        art: list,
        width: Union[int, Literal['auto']] = 'auto',
        height: Union[int, Literal['auto']] = 'auto',
        border_width: int = 2,
        stroke_width: float = 0.5,
        file_type: Literal['PNG', 'JPG', 'GIF', 'WEBP'] = 'PNG',
        font: Optional[AsciiArtFont] = None,
        monochrome: bool = False,
        full_color: bool = False,
        front: Optional[str] = None,
        back: str = '#000000',
    ) -> None:
        if font is None:
            font = AsciiArtFont('courier_prime.ttf')
        char_width, _, line_height = font.get_char_size()

        cols = max(len(line) for line in art)
        rows = len(art)

        img_width = cols * char_width + border_width * 2
        img_height = rows * line_height + border_width * 2

        img = Image.new('RGB', (img_width, img_height), color=back)
        draw = ImageDraw.Draw(img)

        y = border_width - 1
        for line in art:
            x = border_width
            for character in line:
                fg_color = None
                if front:
                    fg_color = front
                elif full_color:
                    fg_color = character['full-hex-color']
                elif monochrome:
                    fg_color = '#FFFFFF'
                else:
                    fg_color = character['terminal-hex-color']

                draw.text((x, y), character['character'], fill=fg_color, font=font.get_font(), stroke_width=stroke_width)
                x += char_width
            y += line_height

        target_width = width if width != 'auto' else img_width
        target_height = height if height != 'auto' else img_height

        if target_width != img_width and height == 'auto':
            target_height = int(target_height * target_width / img_width)
        if target_height != img_height and width == 'auto':
            target_width = int(target_width * target_height / img_height)

        if target_width != img_width or target_height != img_height:
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

        img.save(path, file_type)

    @staticmethod
    def _save_to_html_file(
        path: str,
        art: str,
        styles: str = DEFAULT_STYLES,
        additional_styles: str = '',
        auto_open: bool = False,
    ) -> None:
        html = f"""<!DOCTYPE html>
    <head>
        <title>ASCII art</title>
        <meta name="generator" content="ASCII Magic {AsciiArt.__VERSION__} - https://github.com/LeandroBarone/python-ascii_magic/" />
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
                    cls.cc(f),
                    cls.cc(b),
                    'ASCII_MAGIC',
                    cls.cc(Front.RESET),
                    cls.cc(Back.RESET),
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
        model: str = None,
        api_key: Optional[str] = None,
        debug: bool = False
    ) -> 'AsciiArt':
        image = cls._load_gemini(prompt, model=model, api_key=api_key, debug=debug)
        return AsciiArt(image)

    @classmethod
    def from_swamui(
        cls,
        prompt: str,
        width: int = 1280,
        height: int = 720,
        steps: int = 20,
        raw_input: dict = {},
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

    @classmethod
    def _load_gemini(
        cls,
        prompt: str,
        model: str = None,
        api_key: Optional[str] = None,
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

        if not model:
            model = 'gemini-2.0-flash-preview-image-generation'

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

        if debug:
            with open(str(int(time())) + '_gemini.txt', 'w') as f:
                f.write(str(response))

        for part in response.parts:
            if part.inline_data:
                generated_image = part.as_image()
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
        raw_input: dict = {},
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
