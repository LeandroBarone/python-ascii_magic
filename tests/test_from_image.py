from context import ascii_magic
from PIL import Image

with Image.open('moon.jpg') as img:
	from_image = ascii_magic.from_image(img, columns=200, width_ratio=2.5)

ascii_magic.to_terminal(from_image)