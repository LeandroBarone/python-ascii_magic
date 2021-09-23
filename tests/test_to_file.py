from context import ascii_magic

ascii_art = ascii_magic.from_image_file('lion.jpg', mode=ascii_magic.Modes.ASCII)
ascii_magic.to_file('lion.txt', ascii_art)
