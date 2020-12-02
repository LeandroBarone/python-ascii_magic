from context import ascii_magic

from_file = ascii_magic.from_image_file('chicken_transparent.png')
ascii_magic.to_terminal(from_file)