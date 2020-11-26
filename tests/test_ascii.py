from context import ascii_magic

img = ascii_magic.from_image_file('lion.jpg', columns=100, mode=ascii_magic.Modes.ASCII)
print(img)