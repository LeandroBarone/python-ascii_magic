import colorama
from PIL import Image

import urllib.request
from enum import Enum

CHARS_BY_DENSITY = ' .`-_\':,;^=+/"|)\\<>)iv%xclrs{*}I?!][1taeo7zjLunT#JCwfy325Fp6mqSghVd4EgXPGZbYkOA&8U$@KHDBWNMR0Q'

COLOR_DATA = [
	[(  0,   0,   0), colorama.Fore.LIGHTBLACK_EX, '#111'],
	[(  0,   0, 255), colorama.Fore.BLUE, '#00F'],
	[(  0, 255,   0), colorama.Fore.GREEN, '#0F0'],
	[(255,   0,   0), colorama.Fore.RED, '#F00'],
	[(255, 255, 255), colorama.Fore.WHITE, '#FFF'],
	[(255,   0, 255), colorama.Fore.MAGENTA, '#F0F'],
	[(  0, 255, 255), colorama.Fore.CYAN, '#0FF'],
	[(255, 255,   0), colorama.Fore.YELLOW, '#FF0']
]

PALETTE = [ [[(v/255.0)**2.2 for v in x[0]], x[1], x[2]] for x in COLOR_DATA ]

class Modes(Enum):
	HTML = 'html'
	TERMINAL = 'terminal'
	HTML_TERMINAL = 'html-terminal'


def from_url(url: str, **kwargs) -> str:
	with urllib.request.urlopen(url) as response:
		with Image.open(response) as img:
			return from_image(img, **kwargs)


def from_image_file(img_path: str, **kwargs) -> str:
	with Image.open(img_path) as img:
		return from_image(img, **kwargs)


def from_image(img: Image, columns=120, width_ratio=2, char=None, mode: Modes=Modes.TERMINAL, debug=False) -> str:
	if mode not in Modes:
		raise ValueError('Unknown output mode ' + mode)

	img_w, img_h = img.size
	scalar = img_w*width_ratio / columns
	img_w = int(img_w*width_ratio / scalar)
	img_h = int(img_h / scalar)
	rgb_img = img.resize((img_w, img_h))

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
			# source img is a PNG with a transparency layer.
			# if isinstance(pixel, int):
				# pixel = (pixel, pixel, 255)

			srgb = [ (v/255.0)**2.2 for v in pixel ]
			char = chars[int(brightness * (len(chars) - 1))]
			line += _build_char(char, srgb, brightness, mode)

		lines.append(line)

	if mode == Modes.TERMINAL:
		return '\n'.join(lines) + colorama.Fore.RESET
	elif mode == Modes.HTML or mode == Modes.HTML_TERMINAL:
		return '<br />'.join(lines)


def to_terminal(ascii_art: str) -> None:
	colorama.init()
	print(ascii_art)


def convert_color(rgb: list, brightness: float) -> int:
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
	color = convert_color(srgb, brightness)

	if mode == Modes.TERMINAL:
		return color['term'] + char

	elif mode == Modes.HTML_TERMINAL:
		c = color['hex-term']
		return f'<span style="color: {c}">{char}</span>'

	elif mode == Modes.HTML:
		c = color['hex']
		return f'<span style="color: {c}">{char}</span>'