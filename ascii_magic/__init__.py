import colorama
from PIL import Image

import webbrowser
import urllib.error
import urllib.request
from enum import Enum


__VERSION__ = 1.6


_COLOR_DATA = [
	[(  0,   0,   0), colorama.Fore.LIGHTBLACK_EX, '#222'],
	[(  0,   0, 255), colorama.Fore.BLUE, '#00F'],
	[(  0, 255,   0), colorama.Fore.GREEN, '#0F0'],
	[(255,   0,   0), colorama.Fore.RED, '#F00'],
	[(255, 255, 255), colorama.Fore.WHITE, '#FFF'],
	[(255,   0, 255), colorama.Fore.MAGENTA, '#F0F'],
	[(  0, 255, 255), colorama.Fore.CYAN, '#0FF'],
	[(255, 255,   0), colorama.Fore.YELLOW, '#FF0']
]

PALETTE = [ [[(v/255.0)**2.2 for v in x[0]], x[1], x[2]] for x in _COLOR_DATA ]
CHARS_BY_DENSITY = ' .`-_\':,;^=+/"|)\\<>)iv%xclrs{*}I?!][1taeo7zjLunT#JCwfy325Fp6mqSghVd4EgXPGZbYkOA&8U$@KHDBWNMR0Q'

class Modes(Enum):
	ASCII = 'ASCII'
	TERMINAL = 'TERMINAL'
	HTML = 'HTML'
	HTML_TERMINAL = 'HTML_TERMINAL'

Back = colorama.Back

_colorama_is_init = False


class AsciiArt:
	def __init__(self, image: Image.Image):
		self._image = image

	def to_terminal(self, **kwargs):
		art = from_image(self._image, **kwargs)
		to_terminal(art)

	def to_html_file(self, path: str, mode: Modes = Modes.HTML, **kwargs):
		if mode != Modes.HTML and mode != Modes.HTML_TERMINAL:
			raise ValueError('Mode must be HTML or HTML_TERMINAL')

		art = from_image(self._image, mode=mode, **kwargs)
		to_html_file(path, art, **kwargs)

	def to_file(self, path: str, **kwargs):
		art = from_image(self._image, **kwargs)
		to_file(path, art)


def quick_test() -> None:
	to_terminal(from_url('https://source.unsplash.com/800x600?landscapes')) # type: ignore


# From URL
def _from_url(url: str) -> Image.Image:
	try:
		with urllib.request.urlopen(url) as response:
			return Image.open(response)
	except urllib.error.HTTPError as e:
		raise e from None

def from_url(url: str, **kwargs) -> str:
	img = _from_url(url)
	return from_image(img, **kwargs)

def obj_from_url(url: str) -> AsciiArt:
	return AsciiArt(_from_url(url))


# From image file
def _from_image_file(img_path: str) -> Image.Image:
	return Image.open(img_path)


def from_image_file(img_path: str, **kwargs) -> str:
	img = _from_image_file(img_path)
	return from_image(img, **kwargs)


def obj_from_image_file(img_path: str) -> AsciiArt:
	return AsciiArt(_from_image_file(img_path))


# From clipboard
def _from_clipboard() -> Image.Image:
	try:
		from PIL import ImageGrab
		img = ImageGrab.grabclipboard()
	except (NotImplementedError, ImportError):
		img = from_clipboard_linux()

	if not img:
		raise OSError('The clipboard does not contain an image')

	return img


def from_clipboard_linux() -> Image.Image:
	try:
		import gi # type: ignore
		gi.require_version("Gtk", "3.0") # type: ignore
		from gi.repository import Gtk, Gdk # type: ignore
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
	except:
		raise OSError('The clipboard does not contain an image')

	mode = 'RGB'
	img = Image.frombytes(mode, (w, h), data, 'raw', mode, stride)
	return img


def from_clipboard(**kwargs) -> str:
	img = _from_clipboard()
	return from_image(img, **kwargs)

def obj_from_clipboard() -> AsciiArt:
	return AsciiArt(_from_clipboard())


# From image
def from_image(img, columns=120, width_ratio=2.2, char=None, mode: Modes=Modes.TERMINAL, back: colorama.ansi.AnsiBack = None, debug=False, **kwargs) -> str:
	if mode not in Modes:
		raise ValueError('Unknown output mode ' + str(mode))

	img_w, img_h = img.size
	scalar = img_w*width_ratio / columns
	img_w = int(img_w*width_ratio / scalar)
	img_h = int(img_h / scalar)
	rgb_img = img.resize((img_w, img_h))
	color_palette = img.getpalette()

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
			# getpixel() may return an int, instead of tuple of ints, if the
			# source img is a PNG with a transparency layer
			if isinstance(pixel, int):
				pixel = (pixel, pixel, 255) if color_palette is None else tuple(color_palette[pixel*3:pixel*3 + 3])

			srgb = [ (v/255.0)**2.2 for v in pixel ]
			char = chars[int(brightness * (len(chars) - 1))]
			line += _build_char(char, srgb, brightness, mode)

		if mode == Modes.TERMINAL and back:
			lines.append(back + line + colorama.Back.RESET)
		else:
			lines.append(line)

	if mode == Modes.TERMINAL:
		return '\n'.join(lines) + colorama.Fore.RESET
	elif mode == Modes.ASCII:
		return '\n'.join(lines)
	elif mode == Modes.HTML or mode == Modes.HTML_TERMINAL:
		return '<br />'.join(lines)


def obj_from_image(img: Image.Image) -> AsciiArt:
	return AsciiArt(img)


def to_file(path: str, art: str) -> None:
	with open(path, 'w') as f:
		f.write(art)


def init_terminal() -> None:
	global _colorama_is_init
	if not _colorama_is_init:
		colorama.init()
		_colorama_is_init = True


def to_terminal(ascii_art: str) -> None:
	init_terminal()
	print(ascii_art)


def to_html_file(
	path: str,
	art: str,
	styles: str = 'display: inline-block; border-width: 4px 6px; border-color: black; border-style: solid; background-color:black; font-size: 8px;',
	additional_styles: str= '',
	auto_open: bool = False,
	**kwargs,
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


def _convert_color(rgb: list, brightness: float) -> dict:
	min_distance = 2
	index = 0

	for i in range(len(PALETTE)):
		tmp = [ v*brightness for v in PALETTE[i][0] ]
		distance = _L2_min(tmp, rgb)

		if distance < min_distance:
			index = i
			min_distance = distance

	return {
		'term': PALETTE[index][1],
		'hex-term': PALETTE[index][2],
		'hex': '#{:02x}{:02x}{:02x}'.format(*(int(c*200+55) for c in rgb)),
	}


def _L2_min(v1: list, v2: list) -> float:
    return (v1[0]-v2[0])**2 + (v1[1]-v2[1])**2 + (v1[2]-v2[2])**2


def _build_char(char: str, srgb: list, brightness: float, mode: Modes = Modes.TERMINAL) -> str:
	color = _convert_color(srgb, brightness)

	if mode == Modes.TERMINAL:
		return color['term'] + char
	
	elif mode == Modes.ASCII:
		return char

	elif mode == Modes.HTML_TERMINAL:
		c = color['hex-term']
		return f'<span style="color: {c}">{char}</span>'

	elif mode == Modes.HTML:
		c = color['hex']
		return f'<span style="color: {c}">{char}</span>'
