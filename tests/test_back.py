from context import ascii_magic

ascii_magic.to_terminal(ascii_magic.from_image_file('lion.jpg'))
ascii_magic.to_terminal(ascii_magic.from_image_file('lion.jpg', back=ascii_magic.Back.CYAN))