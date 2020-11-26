from context import ascii_magic
from PIL import Image

with Image.open('picture.jpg') as img:
	from_image = ascii_magic.from_image(img, columns=100, width_ratio=2.6, char='#')

ascii_magic.to_terminal(from_image)