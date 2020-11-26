import colorama
from PIL import Image


CHARS_BY_DENSITY = '" .`-_\':,;^=+/"|)\\<>)iv%xclrs{*}I?!][1taeo7zjLunT#JCwfy325Fp6mqSghVd4EgXPGZbYkOA&8U$@KHDBWNMR0Q'

COLOR_DATA = [
	[(  0,   0,   0), colorama.Fore.LIGHTBLACK_EX],
	[(  0,   0, 255), colorama.Fore.BLUE],
	[(  0, 255,   0), colorama.Fore.GREEN],
	[(255,   0,   0), colorama.Fore.RED],
	[(255, 255, 255), colorama.Fore.WHITE],
	[(255,   0, 255), colorama.Fore.MAGENTA],
	[(  0, 255, 255), colorama.Fore.CYAN],
	[(255, 255,   0), colorama.Fore.YELLOW]
]

PALETTE = [ [[(v/255.0)**2.2 for v in x[0]], x[1]] for x in COLOR_DATA ]


def from_image_file(img_path: str, columns=120, width_ratio=2.5, char=None) -> None:
	with Image.open(img_path) as img:
		return from_image(img, columns, width_ratio, char)


def from_image(img: Image, columns=120, width_ratio=2.5, char=None) -> None:
	img_w, img_h = img.size
	scalar = img_w*width_ratio / columns
	img_w = int(img_w*width_ratio / scalar)
	img_h = int(img_h / scalar)
	rgb_img = img.resize((img_w, img_h))

	grayscale_img = rgb_img.convert("L")
	chars = [char] if char else CHARS_BY_DENSITY

	lines = []
	for h in range(img_h):
		line = ''
		for w in range(img_w):
			# get brightness value
			brightness = grayscale_img.getpixel((w, h)) / 255
			pixel = rgb_img.getpixel((w, h))
			# getpixel() may return an int, instead of tuple of ints, if the
			# source img is a PNG with a transparency layer.
			if isinstance(pixel, int):
				pixel = (pixel, pixel, 255)

			srgb = [ (v/255.0)**2.2 for v in pixel ]
			char_pos = int(brightness * (len(chars) - 1))

			color = convert_color(srgb, brightness)
			line += color + chars[char_pos]
		lines.append(line)

	return '\n'.join(lines) + colorama.Fore.RESET


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

	return PALETTE[index][1]


def _L2_min(v1: list, v2: list) -> float:
    return (v1[0]-v2[0])**2 + (v1[1]-v2[1])**2 + (v1[2]-v2[2])**2