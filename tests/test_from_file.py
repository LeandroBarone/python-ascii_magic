from context import ascii_magic

from_file = ascii_magic.from_image_file('kid.jpg', columns=100, width_ratio=2.6, char='#')
ascii_magic.to_terminal(from_file)