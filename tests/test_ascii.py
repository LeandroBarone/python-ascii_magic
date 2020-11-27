from context import ascii_magic

img = ascii_magic.from_image_file('lion.jpg', columns=200, width_ratio=2.5, mode=ascii_magic.Modes.ASCII)
print(img)